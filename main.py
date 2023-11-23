from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from models import db, ToDo, Tags


# Flask application init
app = Flask(__name__)
app.config['SECRET_KEY'] = "ajsytupofpi394858hg949"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
Bootstrap5(app)

# Database init
db.init_app(app)

with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)





