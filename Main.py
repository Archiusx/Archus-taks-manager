from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.json
    tasks.append(task)
    return jsonify({'status': 'Task added successfully', 'tasks': tasks})

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

import datetime

def schedule_tasks(tasks):
    total_time = 8 * 60  # Total minutes available in a day
    time_per_task = total_time // len(tasks)
    schedule = {}

    current_time = datetime.datetime.now().replace(hour=9, minute=0)  # Start at 9 AM
    for task in tasks:
        end_time = current_time + datetime.timedelta(minutes=time_per_task)
        schedule[task['name']] = (current_time.strftime('%H:%M'), end_time.strftime('%H:%M'))
        current_time = end_time

    return schedule

@app.route('/schedule_tasks', methods=['GET'])
def get_schedule():
    schedule = schedule_tasks(tasks)
    return jsonify(schedule)

progress = {}

@app.route('/update_progress', methods=['POST'])
def update_progress():
    data = request.json
    task_name = data['task_name']
    progress_percent = data['progress']
    progress[task_name] = progress_percent
    return jsonify(progress)

if __name__ == '__main__':
    app.run(debug=True
