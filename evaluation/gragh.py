import matplotlib.pyplot as plt

label = ["normal", "suspend priority", "node startup priority"]
left = [1, 2, 3]


def MakeSpanGragh(normal, preemption, nodeStart):
    value = [normal, preemption, nodeStart]
    graph = plt.bar(left, value, color="blue", linewidth=1, align="center", tick_label=label, width=0.3)
    plt.xticks(fontname="MS Gothic")
    plt.ylabel("makespan (s)", fontname="MS Gothic")

    def autolabel(graph):
        for rect in graph:
            height = rect.get_height()
            plt.annotate(
                "{}".format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    autolabel(graph)
    plt.savefig("./result/makespan.pdf")
    plt.show()


# 電力消費量
def EnergyConsumptionGragh(normal, preemption, nodeStart):
    value = [normal, preemption, nodeStart]
    graph = plt.bar(left, value, color="blue", linewidth=1, align="center", tick_label=label, width=0.3)
    plt.xticks(fontname="MS Gothic")
    plt.ylabel("energy consumption (J)", fontname="MS Gothic")

    def autolabel(graph):
        for rect in graph:
            height = rect.get_height()
            plt.annotate(
                "{}".format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    autolabel(graph)
    plt.savefig("./result/energyConsumption.pdf")
    plt.show()


# 最大電力
def ElectricPowerGragh(normal, preemption, nodeStart):
    value = [normal, preemption, nodeStart]
    plt.xticks(fontname="MS Gothic")
    plt.ylabel("electric power (W)", fontname="MS Gothic")
    plt.xlabel("time (s)", fontname="MS Gothic")
    for i in range(len(label)):
        x = [i for i in range(len(value[i]))]
        y = value[i]
        plt.plot(x, y, label=label[i])
    plt.legend(prop={"family": "MS Gothic"})
    plt.savefig("./result/electricPower.pdf")
    plt.show()


# 締切達成率
def deadlineRatioGragh(preemption, nodeStart):
    y_values = [preemption, nodeStart]
    x_values = [0, 1]
    plt.bar(
        x_values, y_values, color="blue", linewidth=1, align="center", tick_label=[label[1], label[2]], width=0.1
    )
    plt.xticks(fontname="MS Gothic")
    plt.ylabel("deadlineratio (%)", fontname="MS Gothic")
    # plt.legend(prop={"family": "MS Gothic"})
    plt.savefig("./result/deadlineratio.pdf")
    plt.show()
