from basicFunction.basicFunction import JobPlacement
from basicFunction.countNode import countNode
# 通常ジョブ割り当て (割り当てられるか確認、割り当て関数呼び出し、待ちジョブから削除)


def NormalJobAssignment(now, event, Nodes,normalJob_queue):
    for job in normalJob_queue:
        if(job.status ==-1):
            use_nodes = job.nodes
            # ノードが空いているかの確認
            empty_node = countNode(Nodes,0)
            available_num_node = len(empty_node)
            if available_num_node == 0:
                break
            # 空いてるノードに配置
            if available_num_node >= use_nodes:
                JobPlacement(now, empty_node, job, event, Nodes, popNum=0)
