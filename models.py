from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


todo_tag = db.Table('todo_tag',
                    db.Column('todo_id', db.Integer, db.ForeignKey('todo.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class ToDo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    datetime = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Boolean, nullable=False)
    # Relationships
    tags = db.relationship('Tag', secondary=todo_tag, backref='todos')


class Tags(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Relationships

    def __repr__(self):
        return f'<Tag "{self.name}">'



