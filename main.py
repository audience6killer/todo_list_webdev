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
    db.drop_all()
    db.create_all()


# Routes
@app.route('/')
def home():
    active_tasks = db.session.execute(db.Select(ToDo).where(ToDo.status == True)).scalars().all()
    completed_tasks = db.session.execute(db.Select(ToDo).where(ToDo.status == False)).scalars().all()
    return render_template('index.html',
                           active_tasks=active_tasks,
                           completed_tasks=completed_tasks)


@app.route('/new_task', methods=['POST'])
def new_task():
    if request.method == 'POST':
        task_name = request.form['new_task']
        entry = task_name.split('#')
        # We check whether the tags are already in the db
        task_tags = []
        for tag in entry[1:]:
            tag_clean = tag.replace(' ', '')
            tag_search = db.session.execute(db.Select(Tag).where(Tag.name == tag_clean)).scalars().first()
            if tag_search:
                task_tags.append(tag_search)
            else:
                new_tag = Tag(name=tag_clean)
                db.session.add(new_tag)
                task_tags.append(new_tag)

        print(type(task_tags[0]))

        new_todo = ToDo(
            name=entry[0],
            status=True,
        )
        if task_tags:
            for tag in task_tags:
                new_todo.tags.append(tag)

        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))

    return "Nothing yet!"


@app.route('/complete-task/<int:task_id>', methods=['POST', 'GET'])
def complete_task(task_id):
    post_to_complete = db.get_or_404(ToDo, task_id)
    post_to_complete.status = False
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/delete_task/<int:task_id>', methods=['POST', 'GET'])
def delete_task(task_id):
    post_2_delete = db.get_or_404(ToDo, task_id)
    db.session.delete(post_2_delete)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/reactive-task/<int:task_id>', methods=['POST', 'GET'])
def reactive_task(task_id):
    post = db.get_or_404(ToDo, task_id)
    post.status = True
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/sort-by-tag/<string:tag_name>', methods=['POST', 'GET'])
def show_tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    active_tasks = [task for task in tag.todos if task.status]
    completed_tasks = [task for task in tag.todos if not task.status]

    return render_template('tasks_by_tag.html',
                           tag_name=tag_name,
                           active_tasks=active_tasks,
                           completed_tasks=completed_tasks)



if __name__ == "__main__":
    app.run(debug=True)
