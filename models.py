from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


todo_tag = db.Table('todo_tag',
                    db.Column('todo_id', db.Integer, db.ForeignKey('todo.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class ToDo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False)  # True: Active, False: Compleated
    # Relationships
    tags = db.relationship('Tag', secondary=todo_tag, backref='todos')

    def __init__(self, name, status):
        self.name = name
        self.status = status


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Relationships

    def __repr__(self):
        return f'<Tag "{self.name}">'



