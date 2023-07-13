#通常ジョブ割り当て
    def NormalJobAssignment(event,Nodes,empty_node,normalJob_queue):
        remove_idx = []
        for idx, job in enumerate(normalJob_queue):
            use_nodes = job.nodes

            #ノードが空いているかの確認
            available_num_node = len(empty_node)
            if available_num_node == 0:
                break
            #空いてるノードに配置
            if available_num_node >= use_nodes:
                JobPlacement(now,use_nodes,empty_node,job,event,Nodes,popNum=0)
                remove_idx.append(idx)
        #ジョブキューから配置したジョブを削除
        for idx in reversed(remove_idx):
            normalJob_queue.pop(idx)