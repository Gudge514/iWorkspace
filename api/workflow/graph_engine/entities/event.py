class Event:
    def __init__(self, event_type: str, data: dict):
        self.event_type = event_type
        self.data = data

# 示例子类
class NodeStartedEvent(Event):
    def __init__(self, node_id: str):
        super().__init__('NodeStarted', {'node_id': node_id})

class NodeSucceededEvent(Event):
    def __init__(self, node_id: str, output: dict):
        super().__init__('NodeSucceeded', {'node_id': node_id, 'output': output})
