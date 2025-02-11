from typing import Mapping
from workflow.nodes.node_mapping import NodeType

class WorkflowGraph:
    def __init__(self, input_variable: list[str]):
        self.nodes: Mapping[str, NodeType] = {}
        self.data: Mapping[str, dict] = {}
        self.edges = []
        self.input_variable = input_variable

    def add_node(self, node_id: str, node_type: NodeType, node_data: dict):
        """添加节点"""
        self.nodes[node_id] = node_type
        self.data[node_id] = node_data

    def add_edge(self, source_node_id: str, target_node_id: str):
        """添加边"""
        self.edges.append((source_node_id, target_node_id))

    def get_next_nodes(self, node_id: str) -> list[str]:
        """获取给定节点的后续节点"""
        return [target for source, target in self.edges if source == node_id]
