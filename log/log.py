import matplotlib.pyplot as plt


# logを書き出すためのファイル
def LogNormalJob(name, normalJob_queue, urgentJob_queue):
    with open("./log/{}/normalJob.txt".format(name), "w") as file:
        # 通常ジョブを書き込む
        file.write("id,nodes,etime,memory\n")
        for job in normalJob_queue:
            tmp = [job.id, job.nodes, job.etime, job.memory]
            file.write(",".join([str(item) for item in tmp]))
            file.write("\n")
        if len(urgentJob_queue) != 0:
            for job in urgentJob_queue:
                tmp = [job.id, job.nodes, job.etime, job.memory]
                file.write(",".join([str(item) for item in tmp]))
                file.write("\n")


def LogResult(name, result):
    with open("./log/{}/result.txt".format(name), "w") as file:
        file.write("id,startTime,endTime,runNode,status\n")
        for tmp in result:
            file.write(",".join([str(item) for item in tmp]))
            file.write("\n")


def LogNodes(name, now, Nodes):
    with open("./log/{}/Nodes.txt".format(name), "a") as file:
        # 秒を書き込む
        file.write("now:{}\n".format(now))
        tmp = "len:{},".format(len(Nodes))
        for idx, node in enumerate(Nodes):
            if idx == 0:
                pass
            else:
                tmp += ","
            tmp += str(node.status)
        file.write("[{}]\n".format(tmp))


def NodeResult(now, Nodes, nodeResult):
    for node in Nodes:
        try:
            nodeResult[now].append(node.status)
        except:
            nodeResult[now] = [node.status]
    return nodeResult


# 可視化用のツール
def VisualizationJob(result):
    time_intervals = []
    nodes = []
    fig, ax = plt.subplots()
    for item in result:
        start_time = item[1]
        end_time = item[2]
        node_list = item[3]
        for node in node_list:
            ax.barh(node, width=(end_time - start_time), left=start_time)
    plt.xlabel("Time")
    plt.ylabel("Node")
    plt.title("Job status per time")
    plt.tight_layout()
    plt.show()


def VisualizationNode(nodeResult):
    nodecolor = {-22: "g", -21: "g", -1: "w", 0: "k", 1: "y", 2: "k", 21: "r", 22: "r"}
    node_labels = {
        -22: "nodeshutdown",
        -21: "nodestart",
        -1: "shutdown",
        0: "idle",
        1: "run",
        2: "reserved",
        21: "preemption",
        22: "recover",
    }
    legend_entries = []
    past = 0
    fig, ax = plt.subplots()
    while len(nodeResult) != 0:
        now = next(iter(nodeResult))
        Nodes = nodeResult.pop(now)
        for idx, node in enumerate(Nodes):
            if node_labels[node] not in legend_entries:  # 同じラベルのエントリが重複して追加されないようにする
                legend_entries.append(node_labels[node])
                ax.barh(idx, width=(now - past), left=past, color=nodecolor[node], label=node_labels[node])
            else:
                ax.barh(idx, width=(now - past), left=past, color=nodecolor[node])
        past = now
    node
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0))
    plt.ylabel("Node")
    plt.title("node status per time")
    plt.tight_layout()
    plt.show()
