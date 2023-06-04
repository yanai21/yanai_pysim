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

def PreemptionAlgorithm(urgentJob,Nodes,NUM_NODES,available_num_node,use_nodes,now,event,empty_node,dp,breakdp):
        urgentJob.type = "urgent_p"
        # #Nodesから投入されているジョブリストを作成
        # jobSet = set()
        # for job in Nodes:
        #     try:
        #         jobSet.add(job[0])
        #     except:
        #         pass
        # jobList = list(jobSet)
        # #DPの実行
        # dp,breakdp=DP(len(jobList),NUM_NODES,jobList)
        #中断するジョブを選ぶ
        #ほしいノード数があるかの確認
        if(dp[-1][urgentJob.nodes - available_num_node]!=0):
            preemptionJobs=breakdp[-1][urgentJob.nodes - available_num_node]
        else:
            #最小のノード数を探索
            for i in range(urgentJob.nodes - available_num_node,NUM_NODES+1):
                if(dp[-1][i]!=0):
                    preemptionJobs=breakdp[-1][i]
                    break
                if(i==NUM_NODES):
                    print("中断できない")
                    exit()
        #中断開始
        preemptionNode=[]
        for preemptionJob in preemptionJobs:
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
        #緊急ジョブを割り当て (中断したジョブのノード数で実行するために、後ろから配列を参照する)
        # nowに中断時間を加える
        now += PreemptionOverhead(urgentJob.totalPreemptionMemory,writeBandwidth)
        empty_node,urgentJob,event,Nodes=JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=-1)
        return empty_node,urgentJob,event,Nodes,preemptionJobs

def PreemptionRecover(eventJob,Nodes,empty_node,now,preemptionJobs,event):
    #復帰時間
    recover_time = PreemptionOverhead(eventJob.totalPreemptionMemory,readBandwidth)
    #中断ジョブを復帰
    print(preemptionJobs)
    for preemptionJob in preemptionJobs:
        for idx in preemptionJob.runNode:
            Nodes[idx]=[preemptionJob]
            try:
                empty_node.remove(idx)
            except:
                pass
        finish_time = now + recover_time + preemptionJob.leftEtime
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



