from flask_restful import Resource
from flask import request, jsonify, Response
from sqlalchemy import cast, String
import uuid
from workflow.graph_engine.entities.graph import db, Graph, Node, Edge, Viewport
from workflow.graph_engine.entities.workflow_graph import WorkflowGraph
from workflow.nodes.node_mapping import NodeType
from workflow.graph_engine.graph_engine import WorkflowRunner
from workflow.graph_engine.entities.variable import Variable
from concurrent.futures import ThreadPoolExecutor
import traceback

class WorkflowResource(Resource):
    def post(self, graph_id):
        """
        执行工作流
        """
        try:
            # 查询图
            graph = Graph.query.filter_by(id=graph_id).first()

            if not graph:
                return {"message": f"Graph with id {graph_id} not found"}, 404

            # 查询起始节点
            nodes = Node.query.filter_by(graph_id=graph_id).all()
            start_node = [node for node in nodes if node.data["type"] in ["start", "开始"]][0]
            
            graph = WorkflowGraph([])
            
            node_type_mapping = {
                "开始": NodeType.START,
                "start": NodeType.START,
                "结束": NodeType.END,
                "LLM调用": NodeType.LLM
            }
            
            for node in nodes:
                graph.add_node(node.id, node_type_mapping[node.data["type"]], node.data)
            
            for edge in Edge.query.filter_by(graph_id=graph_id).all():
                graph.add_edge(edge.source, edge.target)

            engine = WorkflowRunner(graph, ThreadPoolExecutor(max_workers=4))

            # engine.variable_pool.add(["1", "prompt"], Variable(name="prompt", value="Hello, who are you", selector=["1", "prompt"]))
            # engine.variable_pool.add(["2", "prompt"], Variable(name="prompt", value="Hello there", selector=["2", "prompt"]))
            # engine.variable_pool.add(["3", "prompt"], Variable(name="prompt", value="How are you", selector=["2", "prompt"]))
            
            # engine.run(start_node_id=start_node.id)
            
            # return {"message": "Workflow executed successfully"}, 200
            return Response(engine.run(start_node_id=start_node.id), content_type='text/plain')
            
        except Exception as e:
            print("-"*20)
            print(traceback.format_exc())
            print("-"*20)
            return {"message": traceback.format_exc()}, 500
        