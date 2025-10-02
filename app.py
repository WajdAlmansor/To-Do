from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
# initialize the app with the extension
db = SQLAlchemy(app)


class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'
    
with app.app_context():
    db.create_all()
    

@app.route('/', methods=['POST', 'GET'])
#Home Page
def home():
    # Add Task
    if request.method == 'POST' and 'contentt' in request.form:
        current_task = request.form['contentt']
        new_task = MyTask(content = current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
        
    # Show Tasks
    else:
        tasks = MyTask.query.all()
        return render_template("to-do.html", tasks=tasks)
    

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')

    except Exception as e:
        return f"Error: {e}"
    



@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = MyTask.query.get_or_404(id)

    # checkbox
    if 'complete' in request.form:
        task.completed = True
    else:
        task.completed = False

    # edit text
    if 'content' in request.form:
        new_content = request.form['content'].strip()
        if new_content:
            task.content = new_content

    db.session.commit()
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)