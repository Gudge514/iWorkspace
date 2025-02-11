from extension import db

class Node(db.Model):
    __tablename__ = "nodes"

    id = db.Column(db.String(255), primary_key=True)  # 节点 ID
    graph_id = db.Column(db.String(255), db.ForeignKey("graphs.id"), nullable=False)
    data = db.Column(db.JSON, nullable=False)  # 节点数据
    position_x = db.Column(db.Float, nullable=False)
    position_y = db.Column(db.Float, nullable=False)
    selected = db.Column(db.Boolean, default=False)
    source_position = db.Column(db.String(255), nullable=True)
    target_position = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=True)


class Edge(db.Model):
    __tablename__ = "edges"

    id = db.Column(db.String(255), primary_key=True)  # 边 ID
    graph_id = db.Column(db.String(255), db.ForeignKey("graphs.id"), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    sourceHandle = db.Column(db.String(255), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    targetHandle = db.Column(db.String(255), nullable=False)
    selected = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(255), nullable=True)
    
class Viewport(db.Model):
    __tablename__ = "viewport"
    
    id = db.Column(db.String(255), primary_key=True)
    graph_id = db.Column(db.String(255), db.ForeignKey("graphs.id"), nullable=False)
    zoom = db.Column(db.Float, nullable=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)


class Graph(db.Model):
    __tablename__ = "graphs"

    id = db.Column(db.String(255), primary_key=True)  # 图 ID
    name = db.Column(db.String(255), nullable=True)  # 图标题
    description = db.Column(db.String(255), nullable=True)  # 图描述
    nodes = db.relationship("Node", backref="graph", lazy=True, cascade="all, delete-orphan")
    edges = db.relationship("Edge", backref="graph", lazy=True, cascade="all, delete-orphan")
    viewport = db.relationship("Viewport", backref="graph", lazy=True, cascade="all, delete-orphan")
