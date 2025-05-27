from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timezone
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Initialize the SQLAlchemy database instance
db = SQLAlchemy(app)

# Define the database model for the to-do list
class Todo_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the task
    title = db.Column(db.String(200), nullable=False)  # Task title (required)
    completed = db.Column(db.Boolean, default=False)  # Status of the task (0 = incomplete, 1 = complete)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the task was created
    description = db.Column(db.String(200), nullable=False)  # Task description (required)

    # String representation of the task object
    def __repr__(self):
        return '<Task %r>' % self.id


# Route for the home page, which displays all tasks
@app.route('/', methods=['GET', 'POST'])
def index():
    # Retrieve all tasks from the database, ordered by creation date
    tasks = Todo_list.query.order_by(Todo_list.date_created).all()
    # Render the index.html template and pass the tasks to it
    return render_template('index.html', tasks=tasks)

@app.route('/view/<int:id>', methods=['GET'])
def view(id):
    task_to_view = Todo_list.query.get_or_404(id)
    return render_template('view.html', task= task_to_view )
@app.route('/add', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get the title and description from the form
        title = request.form['title']
        description = request.form['description']
        # Create a new task object
        new_task = Todo_list(title=title, description=description)
        try:
            # Add the new task to the database and commit the changes
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            # Handle any errors that occur during the database operation
            return "There was an issue adding your task"
    else:
        # Render the add.html template for the task creation form
        return render_template('add.html')


# Route for deleting a task
@app.route('/delete/<int:id>')
def delete(id):
    # Retrieve the task to delete by its ID
    task_to_delete = Todo_list.query.get_or_404(id)
    try:
        # Delete the task from the database and commit the changes
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        # Handle any errors that occur during the deletion process
        return "There was a problem deleting that task"


# Route for updating a task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Retrieve the task to update by its ID
    task_to_update = Todo_list.query.get_or_404(id)
    if request.method == 'POST':
        # Update the task's title and description with the form data
        task_to_update.title = request.form['title']
        task_to_update.description = request.form['description']
        try:
            # Commit the changes to the database
            db.session.commit()
            return redirect('/')
        except:
            # Handle any errors that occur during the update process
            return "There was a problem updating that task"
    else:
        # Render the update_test.html template for the task update form
        return render_template('update_test.html', task=task_to_update)


# Route for searching tasks by title
@app.route('/search', methods=['GET'])
def search():
    # Get the search term from the query string
    search_task = request.args.get('search')
    # Filter tasks by title using a case-insensitive partial match
    task_to_search = Todo_list.query.filter(Todo_list.title.ilike(f"%{search_task}%")| Todo_list.description.ilike(f"{search_task}")).all()
    # Print the search term to the console for debugging
    print(f"Search term: {search_task}")
    # Render the index.html template with the filtered tasks
    return render_template('index.html', tasks=task_to_search)
@app.route('/mark_completed/<int:id>' , methods=['POST'])
def mark_completed(id):
    task_to_mark = Todo_list.query.get_or_404(id)
    task_to_mark.completed = True
    try:
        db.session.commit()
        return render_template('view.html', task=task_to_mark)
    except:
        return "Unable to mark complete."

@app.route('/uncompleted', methods=['GET'])
def uncompleted():
    task_uncompleted = request.args.get('uncompleted')
    if task_uncompleted:
        tasks = Todo_list.query.filter_by(completed=False).all()
    else:
        tasks = Todo_list.query.all()
    return render_template('index.html', tasks=tasks )

@app.route('/completed', methods=['GET'])
def completed():
    task_completed = request.args.get('completed')
    if task_completed:
        tasks = Todo_list.query.filter_by(completed=True).all()
    else:
        tasks = Todo_list.query.all()
    return render_template('index.html', tasks=tasks )


# Create the database tables if they don't already exist
with app.app_context():
    db.create_all()

# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)