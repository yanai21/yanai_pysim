import matplotlib.pyplot as plt

label=["平常時","中断優先","ノード起動優先"]
left=[1,2,3]
def MakeSpanGragh(normal,preemption,nodeStart):
    value=[normal,preemption,nodeStart]
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
#電力消費量
def EnergyConsumptionGragh(normal,proposed,preemption,nodeStart):
    value=[normal,proposed,preemption,nodeStart]
    graph = plt.bar(left,value,color="blue", linewidth=1, align="center",tick_label=label,width=0.3)
    plt.xticks(fontname="MS Gothic")
    plt.ylabel("電力消費量 (J)",fontname="MS Gothic")
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
#最大電力
def ElectricPowerGragh(normal,preemption,nodeStart):
    value=[normal,preemption,nodeStart]
    plt.xticks(fontname="MS Gothic")
    plt.ylabel("電力 (W)",fontname="MS Gothic")
    plt.xlabel("時間 (s)",fontname="MS Gothic")
    for i in range (len(label)):
        x = [i for i in range(len(value[i]))]
        y = value[i]
        plt.plot(x, y, label=label[i])
    plt.legend(prop = {"family" : "MS Gothic"})
    plt.show()