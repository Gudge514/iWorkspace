from enum import Enum
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Dict

class NodeRunStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"

class NodeRunResult:
    def __init__(self, node_run_id: str, status: NodeRunStatus, output: Any):
        self.node_run_id = node_run_id
        self.status: NodeRunStatus = status
        self.output: Mapping[str, Any] = output

    def __repr__(self):
        return f"NodeRunResult(node_run_id={self.node_run_id}, status={self.status}, output={self.output})"

    def __eq__(self, other):
        return (
            isinstance(other, NodeRunResult)
            and self.node_run_id == other.node_run_id
            and self.status == other.status
            and self.output == other.output
        )

    def __hash__(self):
        return hash((self.node_run_id, self.status, self.output))
    
class NodeRunEvent:
    """节点运行事件"""
    def __init__(self, event_type: str, data: Optional[Dict[str, Any]] = None):
        self.event_type = event_type
        self.data: NodeRunResult = data or {}
