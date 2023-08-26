from basicFunction.basicFunction import DelEvent


class Node:
    def __init__(self, id, status):
        self.id = id
        self.status = status
        self.type = "node"
        self.shutdownStartTime = 0

    # 最大アイドル時間を設定
    def setShutdownEvent(self, event, now, system):
        self.shutdownStartTime = now + system.maxIdleTime
        try:
            event[self.shutdownStartTime].append(self)
        except:
            event[self.shutdownStartTime] = [self]

    # 設定した最大アイドル用のイベントを削除
    def deleteShutdownEvent(self, event):
        DelEvent(event, self.shutdownStartTime, self)
        self.shutdownStartTime = 0
