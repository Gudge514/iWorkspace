from workflow.graph_engine.entities.event_queue import EventQueue

class EventHandler:
    def __init__(self, event_queue: EventQueue):
        self.event_queue = event_queue

    def process_events(self):
        """持续处理队列中的事件"""
        while True:
            event = self.event_queue.consume()
            if not event:
                continue

            # 简单打印事件
            print(f"Processing event: {event.event_type}, Data: {event.data}")

            # 也可以在这里更新日志、通知用户或做其他动作
