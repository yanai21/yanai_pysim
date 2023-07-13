from basicFunction.basicFunction import JobPlacement

def DP(N,W,DataList,now):
    dp = [[0]*(W+1) for i in range(N+1)] # DPの配列作成
    #Kill対象のジョブ情報が記載される
    BreakDP=[[[]for j in range(W+1)] for i in range(N+1)]
    #比較できるときの関数
    def Compare(dp,i,j,DataList,BreakDP,loss):
        dp[i+1][j] = min(dp[i][j], dp[i][j-DataList[i].nodes]+loss)
        if(dp[i+1][j] == dp[i][j]):
            BreakDP[i+1][j] = BreakDP[i][j].copy()
        else:
            tmp_list=BreakDP[i][j-DataList[i].nodes].copy()
            tmp_list.append(DataList[i])
            BreakDP[i+1][j]=tmp_list.copy()
        return dp,BreakDP
    #比較はできないが追加はできる
    def OnlyAdd(dp,i,j,DataList,BreakDP,loss):
        dp[i+1][j] = dp[i][j-DataList[i].nodes]+loss
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
            loss = now - DataList[i].startTime
            if (j < DataList[i].nodes): # この時点では許容量を超えていないので選択しない
                dp,BreakDP=OnlyCopy(dp,i,j,BreakDP)
            elif (j == DataList[i].nodes): 
                #比較できる時
                if(dp[i][j]!=0):
                    dp,BreakDP=Compare(dp,i,j,DataList,BreakDP,loss)
                #比較対象できないが追加できるとき
                else:
                    dp,BreakDP=OnlyAdd(dp,i,j,DataList,BreakDP,loss)
            else:
                #比較対象ができる時
                if(dp[i][j-DataList[i].nodes]!=0 and dp[i][j]!=0):
                    dp,BreakDP=Compare(dp,i,j,DataList,BreakDP,loss)
                #比較できないが追加できるとき
                elif(dp[i][j-DataList[i].nodes]!=0 and dp[i][j]==0):
                    dp,BreakDP=OnlyAdd(dp,i,j,DataList,BreakDP,loss)
                #比較も追加もできないとき
                else:
                    dp,BreakDP=OnlyCopy(dp,i,j,BreakDP)
    return dp,BreakDP

def KillAlgorithm(urgentJob,Nodes,NUM_NODES,available_num_node,use_nodes,now,event,empty_node,normalJob_queue):
        urgentJob.type = "kill"
        #Nodesから投入されているジョブリストを作成
        jobSet = set()
        for job in Nodes:
            try:
                jobSet.add(job[0])
            except:
                pass
        jobList = list(jobSet)
        #DPの実行
        dp,breakdp=DP(len(jobList),NUM_NODES,jobList,now)
        #killするジョブを選ぶ
        #ほしいノード数があるかの確認
        if(dp[-1][urgentJob.nodes - available_num_node]!=0):
            KillJobs=breakdp[-1][urgentJob.nodes - available_num_node]
        else:
            #最小のノード数を探索
            for i in range(urgentJob.nodes - available_num_node,NUM_NODES+1):
                if(dp[-1][i]!=0):
                    KillJobs=breakdp[-1][i]
                    break
                if(i==NUM_NODES):
                    print("強制終了するできない")
                    exit()
        #強制終了開始
        KillNode=[]
        for KillJob in KillJobs:
            #強制終了するジョブをeventから削除
            event_tmp = event[KillJob.eEndTime]
            event_tmp.remove(KillJob)
            event[KillJob.eEndTime] = event_tmp
            #強制終了した結果、空いたノードの把握
            KillNode.extend(KillJob.runNode)
            #ジョブ情報のリセット
            KillJob.startTime = 0
            KillJob.runNode = []
            #ジョブリストに追加
            normalJob_queue.insert(0,KillJob)
        #Nodesから取り除く
        for idx in reversed(KillNode):
            Nodes[idx]=[]
            empty_node.append(idx)
        #緊急ジョブを割り当て (強制終了したジョブのノード数で実行するために、後ろから配列を参照する)
        # nowに強制終了する時間を加える
        # now += PreemptionOverhead(urgentJob.totalPreemptionMemory,writeBandwidth)
        empty_node,urgentJob,event,Nodes=JobPlacement(now,use_nodes,empty_node,urgentJob,event,Nodes,popNum=-1)
        return empty_node,urgentJob,event,Nodes,normalJob_queue