from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from models import db, ToDo, Tag


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


@app.route('/new_task', methods=['POST'])
def new_task():
    if request.method == 'POST':
        task_name = request.form['new_task']
        if task_name:
            new_todo = ToDo(
                name=task_name,
                status=True,
            )
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for('home'))

    return "Nothing yet!"


if __name__ == "__main__":
    app.run(debug=True)





