import copy
from basicFunction.basicFunction import JobPlacement
from basicFunction.basicFunction import FinishJob

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


def PreemptionAlgorithm(urgentJob, Nodes, now, event, result,system):
    # 実行中のジョブを中断していく
    for preemptionJob in urgentJob.preemptionJobs:
        if preemptionJob.status == 1:
            # 中断に要する時間を計測
            urgentJob.totalPreemptionMemory += preemptionJob.memory
            # 結果の書き込み
            preemptionJob.status = 3
            FinishJob(now, preemptionJob, Nodes, result)
            #eventから中断対象を削除
            estimated_endTime = preemptionJob.startTime + preemptionJob.etime
            event_tmp = event[estimated_endTime]
            event_tmp.remove(preemptionJob)
            event[estimated_endTime] = event_tmp
            #中断対象の残り時間を計測
            leftEtime = preemptionJob.etime - now
            preemptionJob.etime = leftEtime
            ## 緊急ジョブのrunNodeの追加
            for node in preemptionJob.runNode:
                if node.status == 0:
                    node.status =21
                    urgentJob.runNode.append(node)
                else:
                    print("中断できません")
                    exit()
        else:
            print("実行されていないジョブです")
            exit()
        #eventの追加
        finishtime = now + system.preemptionOverhead(urgentJob.totalPreemptionMemory, system.writeBandwidth_mb)
        try:
            urgentJob.event[finishtime].append("NodeStartFinish")
            event[finishtime].append(urgentJob)
        except:
            urgentJob.event[finishtime] = ["NodeStartFinish"]
            event[finishtime] = [urgentJob]
    # preemptionNodes = []
    # urgentJob.method.append("preemption")
    # #緊急ジョブ
    # for preemptionJob in preemptionJobs:
    #     # 終了時刻記入
    #     preemptionJob.endTime = now
    #     # statusの変更
    #     preemptionJob.status = "preemptionJob"
    #     # 結果書き込み
    #     result.append(
    #         [
    #             preemptionJob.id,
    #             preemptionJob.startTime,
    #             preemptionJob.endTime,
    #             preemptionJob.runNode,
    #             preemptionJob.status,
    #             preemptionJob.method,
    #         ]
    #     )
    #     # 残り時間の計測
    #     preemptionJob.leftEtime = preemptionJob.etime - now
    #     event_tmp = event[preemptionJob.eEndTime]
    #     event_tmp.remove(preemptionJob)
    #     event[preemptionJob.eEndTime] = event_tmp
    #     preemptionNodes.extend(preemptionJob.runNode)
    #     # 中断に要する時間を計測
    #     urgentJob.totalPreemptionMemory += preemptionJob.memory
    # # イベントに追加
    # finishtime = now + PreemptionOverhead(urgentJob.totalPreemptionMemory, writeBandwidth)
    # try:
    #     event[finishtime].afppend("preemption")
    # except:
    #     event[finishtime] = ["preemption"]
    # # Nodesから取り除く
    # for idx in reversed(preemptionNodes):
    #     # eventの追加
    #     # Nodesに中断中と明記
    #     Nodes[idx] = ["preemption"]
    # reservedNodes.extend(preemptionNodes)
    # return preemptionJobs, preemptionNodes, reservedNodes


def PreemptionFinish(Nodes, preemptionNodes):
    for idx in preemptionNodes:
        Nodes[idx] = ["reserved"]


def PreemptionRecover(eventJob, Nodes, now, preemptionNodes, event, empty_node):
    # 復帰時間
    recover_time = PreemptionOverhead(eventJob.totalPreemptionMemory, readBandwidth)
    for idx in preemptionNodes:
        Nodes[idx] = ["recover"]
        empty_node.remove(idx)
    finish_time = now + recover_time
    try:
        event[finish_time].append("recover")
    except:
        event[finish_time] = ["recover"]
    event = sorted(event.items())
    event = dict((x, y) for x, y in event)
    preemptionNodes = []


def PreemptionRecoverFinish(Nodes, now, preemptionJobs, event):
    for preemptionJob in preemptionJobs:
        preemptionJob.status = "run"
        preemptionJob.startTime = now
        for idx in preemptionJob.runNode:
            Nodes[idx] = [preemptionJob]
        finish_time = preemptionJob.startTime + preemptionJob.leftEtime
        try:
            event[finish_time].append(preemptionJob)
        except:
            event[finish_time] = [preemptionJob]
        event = sorted(event.items())
        event = dict((x, y) for x, y in event)
        # print(event)
    preemptionJobs = []
    return preemptionJobs, event
