from basicFunction.basicFunction import JobPlacement
from basicFunction.countNode import countNode

# # 通常ジョブ割り当て (割り当てられるか確認、割り当て関数呼び出し、待ちジョブから削除)


def NormalJobAssignment(now, event, Nodes, wait_queue):
    remove_jobList = []
    for job in wait_queue:
        if job.status == -1:
            use_nodes = job.nodes
            # ノードが空いているかの確認
            empty_node = countNode(Nodes, 0)
            available_num_node = len(empty_node)
            if available_num_node == 0:
                break
            # 空いてるノードに配置
            elif available_num_node >= use_nodes:
                remove_jobList.append(job)
                JobPlacement(now, empty_node, job, event, Nodes, popNum=0)
        else:
            print("待ちジョブから割り当てられません")
            exit()

    # remove_jobList に追加されたジョブを wait_queue から削除
    for remove_job in reversed(remove_jobList):
        wait_queue.remove(remove_job)
