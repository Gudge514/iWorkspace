from flask_restful import Resource
from flask import request, jsonify
from workflow.graph_engine.entities.graph import Graph, Node, Edge, Viewport
from extension import db
import uuid
        
class GraphListResource(Resource):
    def post(self):
        """
        新建图
        """
        try:
            # 解析请求 JSON
            graph_data = request.get_json()["graph"]
            if not graph_data or "name" not in graph_data:
                return {"message": "Invalid graph data"}, 400

            # 创建图 ID
            graph_id = "gph_"+str(uuid.uuid4())

            # 创建 Graph 实例
            graph = Graph(id=graph_id)
            graph.name = graph_data["name"]
            if "description" in graph_data and graph_data["description"]:
                graph.description = graph_data["description"]
            else:
                graph.description = ""
            
            db.session.merge(graph)

            # 提交事务
            db.session.commit()
            
            # print("Graph created successfully")

            return {"message": "Graph created successfully", "graph_id": graph_id}, 201

        except Exception as e:
            db.session.rollback()
            print(f"Error creating graph: {str(graph_id)}")
            return {"message": f"Error creating graph: {str(e)}"}, 500


    def get(self):
        """
        获取所有图的列表
        """
        graphs = Graph.query.all()
        response = []
        
        for graph in graphs:
            response.append({
                "id": graph.id,
                "name": graph.name,
                "description": graph.description,
            })
            
        return jsonify(response)
    
class GraphResource(Resource):
    def post(self, graph_id):
        """
        接收图数据并存储到数据库
        """
        try:
            # 解析请求 JSON
            graph_data = request.get_json()["graph"]
            if not graph_data or "nodes" not in graph_data or "edges" not in graph_data:
                return {"message": "Invalid graph data"}, 400

            # 创建图 ID
            graph_id = graph_data.get("id")

            # 创建 Graph 实例
            graph = Graph(id=graph_id)
            db.session.merge(graph)

            existing_graph = Graph.query.filter_by(id=graph_id).first()

            if existing_graph:
                # 如果图存在，删除关联的节点和边
                Node.query.filter_by(graph_id=graph_id).delete()
                Edge.query.filter_by(graph_id=graph_id).delete()
                Viewport.query.filter_by(graph_id=graph_id).delete()
            else:
                # 如果图不存在，创建一个新图
                existing_graph = Graph(id=graph_id)
                db.session.add(existing_graph)

            # 插入新节点
            for node in graph_data["nodes"]:
                new_node = Node(
                    id=node["id"],
                    graph_id=graph_id,
                    data=node.get("data", {}),
                    position_x=node["position"]["x"],
                    position_y=node["position"]["y"],
                    selected=node.get("selected", False),
                    source_position=node.get("sourcePosition"),
                    target_position=node.get("targetPosition"),
                    type=node.get("type"),
                )
                db.session.add(new_node)

            # 插入新边
            for edge in graph_data["edges"]:
                new_edge = Edge(
                    id=edge["id"],
                    graph_id=graph_id,
                    source=edge["source"],
                    sourceHandle=edge.get("sourceHandle"),
                    target=edge["target"],
                    targetHandle=edge.get("targetHandle"),
                    selected=edge.get("selected", False),
                    type=edge.get("type"),
                )
                db.session.add(new_edge)
                
            # 插入视口
            viewport = graph_data.get("viewport")
            if viewport:
                new_viewport = Viewport(
                    id=str(uuid.uuid4()),
                    graph_id=graph_id,
                    zoom=viewport["zoom"],
                    x=viewport["x"],
                    y=viewport["y"],
                )
                db.session.add(new_viewport)

            # 提交事务
            db.session.commit()
            
            # print("Graph saved successfully")
            # print(graph)

            return {"message": "Graph saved successfully", "graph_id": graph_id}, 201

        except Exception as e:
            db.session.rollback()
            print(f"Error saving graph: {str(graph_id)}")
            return {"message": f"Error saving graph: {str(e)}"}, 500

    def get(self, graph_id):
        """
        查询指定 ID 的图数据
        """
        # 查询图
        graph = Graph.query.filter_by(id=graph_id).first()

        if not graph:
            return {"message": f"Graph with id {graph_id} not found"}, 404

        # 获取节点和边数据
        nodes = [
            {
                "id": node.id,
                "data": node.data,
                "position": {"x": node.position_x, "y": node.position_y},
                "selected": node.selected,
                "sourcePosition": node.source_position,
                "targetPosition": node.target_position,
                "type": node.type,
            }
            for node in graph.nodes
        ]

        edges = [
            {
                "id": edge.id,
                "source": edge.source,
                "sourceHandle": edge.sourceHandle,
                "target": edge.target,
                "targetHandle": edge.targetHandle,
                "selected": edge.selected,
                "type": edge.type,
            }
            for edge in graph.edges
        ]
        
        viewport = {
            "zoom": graph.viewport[0].zoom,
            "x": graph.viewport[0].x,
            "y": graph.viewport[0].y,
        }

        # 返回结果
        return jsonify({
            "id": graph.id,
            "nodes": nodes,
            "edges": edges,
            "viewport": viewport,
        })
        
    def delete(self, graph_id):
        """
        删除指定 ID 的图数据
        """
        try:
            # 查询图
            graph = Graph.query.filter_by(id=graph_id).first()

            if not graph:
                return {"message": f"Graph with id {graph_id} not found"}, 404

            # 删除图
            db.session.delete(graph)
            db.session.commit()

            return {"message": "Graph deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            print(f"Error deleting graph: {str(graph_id)}")
            return {"message": f"Error deleting graph: {str(e)}"}, 500