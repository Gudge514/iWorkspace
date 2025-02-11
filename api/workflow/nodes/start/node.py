from workflow.nodes.base.node import BaseNode
from workflow.graph_engine.entities.node_entities import NodeRunResult, NodeRunStatus
from uuid import uuid4
import time

class StartNode(BaseNode):
    """
    起始节点，用于启动工作流
    """
    node_type = "start"
    
    def _run(self):
        output_variables = [param["value"]["variables"] for param in self.config.get("params") if param["type"]=="variable" and not param["value"]["isInput"]][0]
        
        for variable in output_variables:
            self.variable_pool.add([self.node_id, variable["id"]], variable["value"])
            
        return NodeRunResult(node_run_id=self.node_id, status=NodeRunStatus.SUCCEEDED, output=output_variables[0]["value"])