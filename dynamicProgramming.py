import copy
from job import NormalJob
#テスト用のデータ生成
DataList=[]
NUM_Nodes=0
NUM_Jobs=10
for i in range(NUM_Jobs):
    #id,nodes, etime,memory
    job_tmp = NormalJob(i+1,i+1, 3,10)
    NUM_Nodes+=job_tmp.nodes
    DataList.append(job_tmp)

# print(DataList)
# print(NUM_Nodes)



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

dp,breakdp=DP(NUM_Jobs,NUM_Nodes,DataList)
print(dp)
print(breakdp)



