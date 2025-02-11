from workflow.nodes.base.node import BaseNode
from workflow.graph_engine.entities.node_entities import NodeRunResult, NodeRunStatus
from uuid import uuid4
import time

class EndNode(BaseNode):
    """
    结束节点
    """
    node_type = "end"
    
    def _run(self):
        input_variables = [param["value"]["variables"] for param in self.config.get("params") if param["type"]=="variable" and param["value"]["isInput"]][0]
        
        return NodeRunResult(node_run_id=self.node_id, status=NodeRunStatus.SUCCEEDED, output=self.config[input_variables[0]["name"]])