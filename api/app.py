from flask import Flask
from flask_restful import Api
import flask_cors
from controller.graph import GraphResource, GraphListResource
from controller.knowledgeDB import KnowledgeDBResource, KnowledgeDBListResource
from extension import db


# 初始化 Flask 和数据库
app = Flask(__name__)
flask_cors.CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/iWorkspace'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)

# 注册资源
api.add_resource(GraphResource, "/api/graph/<string:graph_id>")
api.add_resource(GraphListResource, "/api/graph")
api.add_resource(KnowledgeDBResource, "/api/knowledgeDB/<string:knowledgeDB_id>")
api.add_resource(KnowledgeDBListResource, "/api/knowledgeDB")

if __name__ == "__main__":

    db.init_app(app)
    with app.app_context():
        db.create_all()  # 创建数据库表
    app.run(debug=True)
