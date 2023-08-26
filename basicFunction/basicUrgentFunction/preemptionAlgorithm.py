import copy
from basicFunction.basicFunction import JobPlacement,FinishJob,DelEvent


# DPの計算
def DP(N, W, DataList):
    dp = [[0] * (W + 1) for i in range(N + 1)]  # DPの配列作成
    # 中断対象のジョブ情報が記載される
    BreakDP = [[[] for j in range(W + 1)] for i in range(N + 1)]

    # 比較できるときの関数
    def Compare(dp, i, j, DataList, BreakDP):
        dp[i + 1][j] = min(dp[i][j], dp[i][j - DataList[i].nodes] + DataList[i].memory)
        if dp[i + 1][j] == dp[i][j]:
            BreakDP[i + 1][j] = BreakDP[i][j].copy()
        else:
            tmp_list = BreakDP[i][j - DataList[i].nodes].copy()
            tmp_list.append(DataList[i])
            BreakDP[i + 1][j] = tmp_list.copy()
        return dp, BreakDP

    # 比較はできないが追加はできる
    def OnlyAdd(dp, i, j, DataList, BreakDP):
        dp[i + 1][j] = dp[i][j - DataList[i].nodes] + DataList[i].memory
        tmp_list = BreakDP[i][j - DataList[i].nodes].copy()
        tmp_list.append(DataList[i])
        BreakDP[i + 1][j] = tmp_list.copy()
        return dp, BreakDP

    # 比較も追加もできない
    def OnlyCopy(dp, i, j, BreakDP):
        dp[i + 1][j] = dp[i][j]  # ただ選択はしていないが、今回の情報をそのままi+1の方へ移す
        BreakDP[i + 1][j] = BreakDP[i][j].copy()
        return dp, BreakDP

    # ジョブ数のループ
    for i in range(N):
        # ノード数のループ
        for j in range(W + 1):
            if j < DataList[i].nodes:  # この時点では許容量を超えていないので選択しない
                dp, BreakDP = OnlyCopy(dp, i, j, BreakDP)
            elif j == DataList[i].nodes:
                # 比較できる時
                if dp[i][j] != 0:
                    dp, BreakDP = Compare(dp, i, j, DataList, BreakDP)
                # 比較対象できないが追加できるとき
                else:
                    dp, BreakDP = OnlyAdd(dp, i, j, DataList, BreakDP)
            else:
                # 比較対象ができる時
                if dp[i][j - DataList[i].nodes] != 0 and dp[i][j] != 0:
                    dp, BreakDP = Compare(dp, i, j, DataList, BreakDP)
                # 比較できないが追加できるとき
                elif dp[i][j - DataList[i].nodes] != 0 and dp[i][j] == 0:
                    dp, BreakDP = OnlyAdd(dp, i, j, DataList, BreakDP)
                # 比較も追加もできないとき
                else:
                    dp, BreakDP = OnlyCopy(dp, i, j, BreakDP)
    return dp, BreakDP


def PreemptionAlgorithm(urgentJob, Nodes, now, event, result, system):
    # 実行中のジョブを中断していく
    for preemptionJob in urgentJob.preemptionJobs:
        if preemptionJob.status == 1:
            # 中断に要する時間を計測
            urgentJob.totalPreemptionMemory += preemptionJob.memory
            # 結果の書き込み
            preemptionJob.status = 3
            FinishJob(now, preemptionJob, Nodes, result,event,system)
            # eventから中断対象を削除
            estimated_endTime = preemptionJob.startTime + preemptionJob.etime
            # event = DelEvent(event,estimated_endTime,preemptionJob)
            event_tmp = event[estimated_endTime]
            event_tmp.remove(preemptionJob)
            if len(event_tmp) != 0:
                event[estimated_endTime] = event_tmp
            else:
                event.pop(estimated_endTime)
            # 中断対象の残り時間を計測
            leftEtime = preemptionJob.etime - now
            preemptionJob.etime = leftEtime
            ## 緊急ジョブのrunNodeの追加
            for node in preemptionJob.runNode:
                if node.status == 0:
                    node.status = 21
                    urgentJob.runNode.append(node)
                else:
                    print("中断できません")
                    exit()
        else:
            print("実行されていないジョブです")
            exit()
    # eventの追加
    finishtime = now + system.preemptionOverhead(urgentJob.totalPreemptionMemory, system.writeBandwidth_mb)
    try:
        urgentJob.event[finishtime].append("preemptionFinish")
        event[finishtime].append(urgentJob)
    except:
        urgentJob.event[finishtime] = ["preemptionFinish"]
        event[finishtime] = [urgentJob]


def PreemptionFinish(urgentJob):
    for preemptionJob in urgentJob.preemptionJobs:
        for node in preemptionJob.runNode:
            if node.status == 21:
                node.status = 2
            else:
                print("中断終了できない")
                exit()


def PreemptionRecover(urgentJob, event, now, system):
    # 復帰時間
    finishtime = now + system.preemptionOverhead(urgentJob.totalPreemptionMemory, system.readBandwidth_mb)
    for preemptionJob in urgentJob.preemptionJobs:
        for node in preemptionJob.runNode:
            if node.status == 0:
                node.status = 22
            else:
                print("中断ジョブを復帰できません")
                exit()
    try:
        urgentJob.event[finishtime].append("preemptionRecoverFinish")
        event[finishtime].append(urgentJob)
    except:
        urgentJob.event[finishtime] = ["preemptionRecoverFinish"]
        event[finishtime] = [urgentJob]


def PreemptionRecoverFinish(urgentJob, now, event):
    for preemptionJob in urgentJob.preemptionJobs:
        etime = preemptionJob.etime
        if preemptionJob.status == 3:
            preemptionJob.startTime = now
            preemptionJob.status = 1
            finish_time = now + etime
            for node in preemptionJob.runNode:
                if node.status == 22:
                    node.status =1
                else:
                    print("再開できません")
                    exit()
            try:
                event[finish_time].append(preemptionJob)
            except:
                event[finish_time] = [preemptionJob]    
        else:
            print("正しく中断されていないジョブです")
            exit()
