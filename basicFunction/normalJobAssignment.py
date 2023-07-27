from basicFunction.basicFunction import JobPlacement
from basicFunction.countAvailableNode import countAvaiableNode
# 通常ジョブ割り当て (割り当てられるか確認、割り当て関数呼び出し、待ちジョブから削除)


def NormalJobAssignment(now, event, Nodes,normalJob_queue):
    remove_idx = []
    for idx, job in enumerate(normalJob_queue):
        use_nodes = job.nodes
        # ノードが空いているかの確認
        empty_node = countAvaiableNode(Nodes)
        available_num_node = len(empty_node)
        if available_num_node == 0:
            break
        # 空いてるノードに配置
        if available_num_node >= use_nodes:
            JobPlacement(now, empty_node, job, event, Nodes, popNum=0)
            remove_idx.append(idx)
    # ジョブキューから配置したジョブを削除
    for idx in reversed(remove_idx):
        normalJob_queue.pop(idx)
    return normalJob_queue
