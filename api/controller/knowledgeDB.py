from flask_restful import Resource
from flask import request, jsonify
from workflow.graph_engine.entities.knowledgeDB import KnowledgeDB
from extension import db
import uuid

class KnowledgeDBListResource(Resource):
    def post(self):
        """
        新建知识库
        """
        try:
            # 解析请求 JSON
            knowledgeDB_data = request.get_json()["knowledgeDB"]
            if not knowledgeDB_data or "name" not in knowledgeDB_data:
                return {"message": "Invalid knowledgeDB data"}, 400

            # 创建知识库 ID
            knowledgeDB_id = "kdb_"+str(uuid.uuid4())
            
            if "type" not in knowledgeDB_data:
                knowledgeDB_data["type"] = "vector"
            
            if "language" not in knowledgeDB_data:
                knowledgeDB_data["language"] = "en"

            # 创建 KnowledgeDB 实例
            knowledgeDB = KnowledgeDB(
                id=knowledgeDB_id,
                name=knowledgeDB_data["name"],
                description=knowledgeDB_data.get("description"),
                type=knowledgeDB_data["type"],
                # files=knowledgeDB_data["files"],
                # documents=knowledgeDB_data["documents"],
                language=knowledgeDB_data["language"],
                config=knowledgeDB_data.get("config"),
            )
            db.session.add(knowledgeDB)
            db.session.commit()

            return {"knowledgeDB": knowledgeDB.to_dict()}, 201
        except Exception as e:
            return {"message": str(e)}, 500
        
    def get(self):
        """
        获取所有知识库的列表
        """
        knowledgeDBs = KnowledgeDB.query.all()
        response = []
        
        for knowledgeDB in knowledgeDBs:
            response.append({
                "id": knowledgeDB.id,
                "name": knowledgeDB.name,
                "description": knowledgeDB.description,
                "type": knowledgeDB.type,
                "language": knowledgeDB.language,
            })
            
        return jsonify(response)
    
class KnowledgeDBResource(Resource):
    def get(self, knowledgeDB_id):
        """
        获取知识库数据
        """
        knowledgeDB = KnowledgeDB.query.filter_by(id=knowledgeDB_id).first()
        
        if not knowledgeDB:
            return {"message": f"KnowledgeDB with id {knowledgeDB_id} not found"}, 404
        
        return {"knowledgeDB": knowledgeDB.to_dict()}
    
    def put(self, knowledgeDB_id):
        """
        更新知识库数据
        """
        knowledgeDB = KnowledgeDB.query.filter_by(id=knowledgeDB_id).first()
        
        if not knowledgeDB:
            return {"message": f"KnowledgeDB with id {knowledgeDB_id} not found"}, 404
        
        knowledgeDB_data = request.get_json()["knowledgeDB"]
        
        if "name" in knowledgeDB_data:
            knowledgeDB.name = knowledgeDB_data["name"]
        if "description" in knowledgeDB_data:
            knowledgeDB.description = knowledgeDB_data["description"]
        if "type" in knowledgeDB_data:
            knowledgeDB.type = knowledgeDB_data["type"]
        if "language" in knowledgeDB_data:
            knowledgeDB.language = knowledgeDB_data["language"]
        if "config" in knowledgeDB_data:
            knowledgeDB.config = knowledgeDB_data["config"]
        
        db.session.commit()
        
        return {"knowledgeDB": knowledgeDB.to_dict()}
    
    def delete(self, knowledgeDB_id):
        """
        删除知识库
        """
        knowledgeDB = KnowledgeDB.query.filter_by(id=knowledgeDB_id).first()
        
        if not knowledgeDB:
            return {"message": f"KnowledgeDB with id {knowledgeDB_id} not found"}, 404
        
        db.session.delete(knowledgeDB)
        db.session.commit()
        
        return {"message": "KnowledgeDB deleted successfully"}