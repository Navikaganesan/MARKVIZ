from flask import Flask, request, render_template_string, redirect, flash
import pandas as pd
import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter

app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
ALLOWED_EXTENSIONS = {'csv'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MARKVIZ</title>
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/201/201623.png" type="image/png">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">
    <div class="container mx-auto px-6 py-12 max-w-4xl">
        <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">MARKVIZ</h1>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded-lg">
                <ul>
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
                </ul>
            </div>
          {% endif %}
        {% endwith %}

        <div class="bg-white p-8 rounded-lg shadow-lg mb-10">
            <h2 class="text-2xl font-semibold text-gray-800 mb-6">Option 1: Upload CSV File</h2>
            <form action="/result" method="POST" enctype="multipart/form-data">
                <input type="file" name="file" accept=".csv" required class="mb-4 block w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-6 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100">
                <input type="submit" value="Upload and Analyze" class="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 transition duration-200">
            </form>
        </div>

        <hr class="my-10 border-gray-300">

        <div class="bg-white p-8 rounded-lg shadow-lg">
            <h2 class="text-2xl font-semibold text-gray-800 mb-6">Option 2: Enter Student Marks Manually</h2>
            <form id="numStudentsForm" action="/manual_form" method="POST" class="mb-6">
                <label class="block text-gray-700 font-semibold mb-2">Number of Students:</label>
                <input type="number" id="num_students" name="num_students" min="1" max="100" required class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4">
                <input type="submit" value="Generate Form" class="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 transition duration-200">
            </form>
        </div>
    </div>
    <footer class="text-center text-gray-500 py-6">
        © 2025 Markviz App
    </footer>
</body>
</html>
'''

manual_form_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enter Student Details</title>
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/201/201623.png" type="image/png">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">
    <div class="container mx-auto px-6 py-12 max-w-4xl">
        <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Enter Student Details</h1>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded-lg">
                <ul>
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
                </ul>
            </div>
          {% endif %}
        {% endwith %}

        <div class="bg-white p-8 rounded-lg shadow-lg">
            <h2 class="text-2xl font-semibold text-gray-800 mb-6">Enter Details for {{ num_students }} Student(s)</h2>
            <form action="/result" method="POST">
                {% for i in range(1, num_students + 1) %}
                    <div class="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-gray-700 font-semibold mb-2">Student {{ i }} Name:</label>
                            <input type="text" name="name{{ i }}" required class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        </div>
                        <div>
                            <label class="block text-gray-700 font-semibold mb-2">Marks:</label>
                            <input type="number" name="marks{{ i }}" required step="any" min="0" max="100" class="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        </div>
                    </div>
                {% endfor %}
                <input type="submit" value="Analyze Manually" class="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 transition duration-200">
            </form>
        </div>
        <a href="/" class="inline-block mt-6 bg-gray-600 text-white py-3 px-6 rounded-lg hover:bg-gray-700 transition duration-200">← Back to Input</a>
    </div>
    <footer class="text-center text-gray-500 py-6">
        © 2025 Markviz App
    </footer>
</body>
</html>
'''

result_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Result</title>
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/201/201623.png" type="image/png">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">
    <div class="container mx-auto px-6 py-12 max-w-4xl">
        <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Student Report</h1>
        <div class="bg-white p-8 rounded-lg shadow-lg mb-10">
            <table class="w-full border-collapse">
                <thead>
                    <tr class="bg-indigo-600 text-white">
                        <th class="p-4 text-left">Name</th>
                        <th class="p-4 text-center">Marks</th>
                        <th class="p-4 text-center">Grade</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr class="{% if loop.index % 2 == 0 %}bg-gray-50{% else %}bg-white{% endif %}">
                        <td class="p-4 border-b">{{ student.name }}</td>
                        <td class="p-4 border-b text-center">{{ student.marks }}</td>
                        <td class="p-4 border-b text-center" style="color:
                            {% if student.grade.startswith('A+') %}green
                            {% elif student.grade.startswith('A') %}blue
                            {% elif student.grade.startswith('B') %}#f59e0b
                            {% elif student.grade.startswith('C') %}#f97316
                            {% elif student.grade.startswith('D') %}#dc2626
                            {% else %}red
                            {% endif %}
                        ;">{{ student.grade }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="bg-white p-8 rounded-lg shadow-lg mb-10">
            <h3 class="text-2xl font-semibold text-gray-800 mb-4">Summary</h3>
            <p class="text-gray-700 mb-2"><strong>Total Students:</strong> {{ students|length }}</p>
            <p class="text-gray-700 mb-2"><strong>Class Average:</strong> {{ average }}</p>
            <p class="text-gray-700 mb-2"><strong>Topper(s):</strong> {{ topper }}</p>
            <p class="text-gray-700"><strong>Lowest Scorer(s):</strong> {{ lowest }}</p>
        </div>

        <div class="bg-white p-8 rounded-lg shadow-lg mb-10">
            <h3 class="text-2xl font-semibold text-gray-800 mb-4">Student Marks Bar Chart</h3>
            <img src="data:image/png;base64,{{ bar_chart }}" alt="Bar Chart" class="w-full max-w-3xl mx-auto rounded-lg">
        </div>
        <div class="bg-white p-8 rounded-lg shadow-lg mb-10">
            <h3 class="text-2xl font-semibold text-gray-800 mb-4">Grade Distribution Pie Chart</h3>
            <img src="data:image/png;base64,{{ pie_chart }}" alt="Pie Chart" class="w-full max-w-md mx-auto rounded-lg">
        </div>

        <a href="/" class="inline-block bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 transition duration-200">← Back to Input</a>
    </div>
    <footer class="text-center text-gray-500 py-6">
        © 2025 Markviz App
    </footer>
</body>
</html>
'''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_grade(marks):
    if marks >= 90:
        return 'A+'
    elif marks >= 75:
        return 'A'
    elif marks >= 60:
        return 'B'
    elif marks >= 50:
        return 'C'
    elif marks >= 35:
        return 'D'
    else:
        return 'F (Fail)'

def generate_bar_chart(students):
    names = [student['name'] for student in students]
    marks = [student['marks'] for student in students]
    
    plt.figure(figsize=(8, 5))  # Adjusted for laptop view
    plt.bar(names, marks, color='indigo')
    plt.xlabel('Students', fontsize=12)
    plt.ylabel('Marks', fontsize=12)
    plt.title('Student Marks Distribution', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_pie_chart(students):
    grades = [student['grade'] for student in students]
    grade_counts = Counter(grades)
    labels = list(grade_counts.keys())
    sizes = list(grade_counts.values())
    colors = ['#16a34a', '#3b82f6', '#f59e0b', '#f97316', '#dc2626', '#ef4444']
    
    plt.figure(figsize=(6, 6))  # Adjusted for laptop view
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Grade Distribution', fontsize=14)
    plt.axis('equal')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/manual_form', methods=['POST'])
def manual_form():
    try:
        num_students = int(request.form.get('num_students'))
        if num_students < 1 or num_students > 100:
            flash("Number of students must be between 1 and 100.")
            return redirect('/')
        return render_template_string(manual_form_html, num_students=num_students)
    except ValueError:
        flash("Please enter a valid number of students.")
        return redirect('/')

@app.route('/result', methods=['POST'])
def result():
    student_data = []
    total_marks = 0

    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                df = pd.read_csv(filepath)
                if 'Name' not in df.columns or 'Marks' not in df.columns:
                    flash("CSV must contain 'Name' and 'Marks' columns.")
                    return redirect('/')
                
                for _, row in df.iterrows():
                    name = str(row['Name']).strip()
                    try:
                        marks = float(row['Marks'])
                        if not 0 <= marks <= 100:
                            continue
                        grade = get_grade(marks)
                        student_data.append({'name': name, 'marks': marks, 'grade': grade})
                        total_marks += marks
                    except (ValueError, TypeError):
                        continue
            except Exception as e:
                flash("Failed to read CSV file.")
                return redirect('/')
        else:
            flash("Invalid file format. Please upload a .csv file.")
            return redirect('/')
    else:
        i = 1
        while f'name{i}' in request.form:
            name = request.form.get(f'name{i}')
            try:
                marks = float(request.form.get(f'marks{i}', 0))
                if not 0 <= marks <= 100:
                    flash(f"Marks for {name} must be between 0 and 100.")
                    return redirect('/')
                grade = get_grade(marks)
                student_data.append({'name': name, 'marks': marks, 'grade': grade})
                total_marks += marks
            except ValueError:
                flash(f"Invalid marks for {name}.")
                return redirect('/')
            i += 1

    if not student_data:
        flash("No valid student data found.")
        return redirect('/')

    average = round(total_marks / len(student_data), 2)
    
    # Find highest and lowest marks
    marks_list = [student['marks'] for student in student_data]
    max_marks = max(marks_list) if marks_list else 0
    min_marks = min(marks_list) if marks_list else 0
    
    # Collect all students with highest and lowest marks
    toppers = [student for student in student_data if student['marks'] == max_marks]
    lowest_scorers = [student for student in student_data if student['marks'] == min_marks]
    
    # Format names and marks for display
    topper_display = ", ".join([f"{student['name']} ({student['marks']})" for student in toppers])
    lowest_display = ", ".join([f"{student['name']} ({student['marks']})" for student in lowest_scorers])

    bar_chart = generate_bar_chart(student_data)
    pie_chart = generate_pie_chart(student_data)

    return render_template_string(
        result_html,
        students=student_data,
        average=average,
        topper=topper_display,
        lowest=lowest_display,
        bar_chart=bar_chart,
        pie_chart=pie_chart
    )

if __name__ == '__main__':
    app.run(debug=True)
