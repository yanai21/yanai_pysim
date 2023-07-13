#logを書き出すためのファイル
def LogNormalJob(name,normalJob_queue,urgentJob_queue):
    with open('./log/{}/normalJob.txt'.format(name), 'w') as file:
        # 通常ジョブを書き込む
        file.write("id,nodes,etime\n")
        for job in normalJob_queue:
            tmp = [job.id,job.nodes,job.etime]
            file.write(','.join([str(item) for item in tmp]))
            file.write("\n")
        if(len(urgentJob_queue)!=0):
            for job in urgentJob_queue:
                tmp = [job.id,job.nodes,job.etime]
                file.write(','.join([str(item) for item in tmp]))
                file.write("\n")
def LogResult(name,result):
    with open('./log/{}/result.txt'.format(name), 'w') as file:
        file.write("id,startTime,endTime,runNode,status,method\n")
        for tmp in result:
            file.write(','.join([str(item) for item in tmp]))
            file.write("\n")
def LogNodes(name,now,Nodes):
    with open('./log/{}/Nodes.txt'.format(name), 'a') as file:
        # 秒を書き込む
        file.write("now:{}\n".format(now))
        tmp="len:{},".format(len(Nodes))
        for idx,node in enumerate(Nodes):
            if(idx ==0):
                pass
            else:
                tmp += ","
            if(node ==[]):
                tmp +="empty"
            elif(type(node[0])==str):
                tmp +="{}".format(node[0])
            else:
                tmp +="id:{}".format(node[0].id)
        file.write("[{}]\n".format(tmp))