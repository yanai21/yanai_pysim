import copy
from basicFunction import JobPlacement
from model import PreemptionOverhead
from system import writeBandwidth,readBandwidth

#DPの計算
def DP(N,W,DataList):
    dp = [[0]*(W+1) for i in range(N+1)] # DPの配列作成
    #中断対象のジョブ情報が記載される
    BreakDP=[[[]for j in range(W+1)] for i in range(N+1)]
    #比較できるときの関数
    def Compare(dp,i,j,DataList,BreakDP):
        dp[i+1][j] = min(dp[i][j], dp[i][j-DataList[i].nodes]+DataList[i].memory)
        if(dp[i+1][j] == dp[i][j]):
            BreakDP[i+1][j] = BreakDP[i][j].copy()
        else:
            tmp_list=BreakDP[i][j-DataList[i].nodes].copy()
            tmp_list.append(DataList[i])
            BreakDP[i+1][j]=tmp_list.copy()
        return dp,BreakDP
    #比較はできないが追加はできる
    def OnlyAdd(dp,i,j,DataList,BreakDP):
        dp[i+1][j] = dp[i][j-DataList[i].nodes]+DataList[i].memory
        tmp_list=BreakDP[i][j-DataList[i].nodes].copy()
        tmp_list.append(DataList[i])
        BreakDP[i+1][j]=tmp_list.copy()
        return dp,BreakDP
    #比較も追加もできない
    def OnlyCopy(dp,i,j,BreakDP):
        dp[i+1][j] = dp[i][j] # ただ選択はしていないが、今回の情報をそのままi+1の方へ移す
        BreakDP[i+1][j] = BreakDP[i][j].copy()
        return dp,BreakDP
    #ジョブ数のループ
    for i in range(N):
        #ノード数のループ
        for j in range(W+1):
            if (j < DataList[i].nodes): # この時点では許容量を超えていないので選択しない
                dp,BreakDP=OnlyCopy(dp,i,j,BreakDP)
            elif (j == DataList[i].nodes): 
                #比較できる時
                if(dp[i][j]!=0):
                    dp,BreakDP=Compare(dp,i,j,DataList,BreakDP)
                #比較対象できないが追加できるとき
                else:
                    dp,BreakDP=OnlyAdd(dp,i,j,DataList,BreakDP)
            else:
                #比較対象ができる時
                if(dp[i][j-DataList[i].nodes]!=0 and dp[i][j]!=0):
                    dp,BreakDP=Compare(dp,i,j,DataList,BreakDP)
                #比較できないが追加できるとき
                elif(dp[i][j-DataList[i].nodes]!=0 and dp[i][j]==0):
                    dp,BreakDP=OnlyAdd(dp,i,j,DataList,BreakDP)
                #比較も追加もできないとき
                else:
                    dp,BreakDP=OnlyCopy(dp,i,j,BreakDP)
    return dp,BreakDP

def PreemptionAlgorithm(urgentJob,Nodes,use_nodes,now,event,empty_node,preemptionJobs,result):
        urgentJob.status.append("preemption")
        #中断開始
        preemptionNode=[]
        for preemptionJob in preemptionJobs:
            #statusを追加
            preemptionJob.status = "preemption"
            #終了時刻記入
            preemptionJob.endTime=now
            #結果書き込み
            result.append([preemptionJob.id,preemptionJob.startTime,preemptionJob.endTime,preemptionJob.runNode,preemptionJob.status])
            #残り時間の計測
            preemptionJob.leftEtime = preemptionJob.etime - now
            #中断ジョブをeventから削除
            event_tmp = event[preemptionJob.eEndTime]
            event_tmp.remove(preemptionJob)
            event[preemptionJob.eEndTime] = event_tmp
            #中断した結果、空いたノードの把握
            preemptionNode.extend(preemptionJob.runNode)
            #中断に要する時間を計測
            urgentJob.totalPreemptionMemory += preemptionJob.memory
        #Nodesから取り除く
        for idx in reversed(preemptionNode):
            Nodes[idx]=[]
            empty_node.append(idx)
        return empty_node,urgentJob,event,Nodes,preemptionJobs,result

def PreemptionRecover(eventJob,Nodes,empty_node,now,preemptionJobs,event):
    #復帰時間
    recover_time = PreemptionOverhead(eventJob.totalPreemptionMemory,readBandwidth)
    #中断ジョブを復帰
    print(preemptionJobs)
    for preemptionJob in preemptionJobs:
        #情報の変更
        preemptionJob.status = "recover"
        preemptionJob.startTime = now + recover_time
        for idx in preemptionJob.runNode:
            Nodes[idx]=[preemptionJob]
            try:
                empty_node.remove(idx)
            except:
                pass
        finish_time = preemptionJob.startTime + preemptionJob.leftEtime
        try:
            event[finish_time].append(preemptionJob)
        except:
            event[finish_time] = [preemptionJob]
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)
    preemptionJobs=[]
    return eventJob,Nodes,empty_node,preemptionJobs,event


# #テスト用のデータ生成
# from job import NormalJob
# DataList=[]
# NUM_Nodes=0
# NUM_Jobs=10
# for i in range(NUM_Jobs):
#     #id,nodes, etime,memory
#     job_tmp = NormalJob(i+1,i+1, 3,10)
#     NUM_Nodes+=job_tmp.nodes
#     DataList.append(job_tmp)

# dp,breakdp=DP(NUM_Jobs,NUM_Nodes,DataList)
# print(dp)
# print(breakdp)


