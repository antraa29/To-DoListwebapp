from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Add your MySQL password
    database="todo_app"
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    conn.commit()
    return redirect('/')

@app.route('/toggle_status/<int:task_id>')
def toggle_status(task_id):
    cursor.execute("SELECT status FROM tasks WHERE id = %s", (task_id,))
    current_status = cursor.fetchone()['status']
    new_status = 'pending' if current_status == 'completed' else 'completed'
    cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (new_status, task_id))
    conn.commit()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
