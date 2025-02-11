import queue
from workflow.graph_engine.entities.event import Event

class EventQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def publish(self, event: Event):
        """将事件发布到队列中"""
        self.queue.put(event)

    def consume(self) -> Event:
        """消费事件"""
        try:
            return self.queue.get(block=True, timeout=5)  # 等待消费
        except queue.Empty:
            return None
