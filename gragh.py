import matplotlib.pyplot as plt

label=["平常時","提案手法","中断優先","ノード起動優先"]
left=[1,2,3,4]
def MakeSpanGragh(normal,proposed,preemption,nodeStart):
    value=[normal,proposed,preemption,nodeStart]
    graph = plt.bar(left,value,color="blue", linewidth=1, align="center",tick_label=label,width=0.3)
    plt.xticks(fontname="MS Gothic")
    plt.ylabel("メイクスパン (s)",fontname="MS Gothic")
    def autolabel(graph):
        for rect in graph:
            height = rect.get_height()
            plt.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom')
    autolabel(graph)
    plt.show()
def EnergyConsumptionGragh(normal,proposed,preemption,nodeStart):
    value=[normal,proposed,preemption,nodeStart]
    graph = plt.bar(left,value,color="blue", linewidth=1, align="center",tick_label=label,width=0.3)
    plt.xticks(fontname="MS Gothic")
    plt.ylabel("電力消費量 (W)",fontname="MS Gothic")
    def autolabel(graph):
        for rect in graph:
            height = rect.get_height()
            plt.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom')
    autolabel(graph)
    plt.show()