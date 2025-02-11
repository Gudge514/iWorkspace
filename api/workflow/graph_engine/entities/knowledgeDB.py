from extension import db

class KnowledgeDB(db.Model):
    
    __tablename__ = "knowledgeDB"
    
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=False)
    files = db.Column(db.JSON, nullable=False)
    documents = db.Column(db.JSON, nullable=False)
    language = db.Column(db.String(255), nullable=False)
    config = db.Column(db.JSON, nullable=True)