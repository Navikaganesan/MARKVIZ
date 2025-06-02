Markviz: Student Marks Analyzer & Visualizer
Markviz is a web-based application built with Flask that simplifies the process of analyzing and visualizing student marks. Whether you're a teacher, student, or education enthusiast, Markviz helps you gain instant insights into academic performance through clean analytics and visual reports.

The Markviz Advantage
Markviz streamlines student marks analysis by allowing users to upload or input data and receive clear performance metrics and charts. Designed with ease of use and functionality in mind, Markviz is suitable for:

Teachers evaluating class performance

Students reviewing their academic progress

Education professionals conducting research

Developers building educational tools

Key Features
CSV and Manual Input
Upload a .csv file or manually enter student names and marks through the form.

Automatic Analysis
Processes and displays:

Class average

Highest and lowest scores

Grade assignment based on score thresholds

Visual Insights
Automatically generates:

Bar Chart of student marks

Pie Chart of grade distribution

Powered by matplotlib, these charts provide immediate visual understanding.

Download and Reset Tools
Input validation for clean data handling

Options to re-upload or clear datasets

Modern, responsive interface styled with TailwindCSS

How to Use Markviz
Accessing the App
Run locally by navigating to:
http://127.0.0.1:5000/

You can also deploy it using your preferred hosting platform.

Interface Overview
Header
Application name: Markviz

Upload or manual entry toggle

Clean, accessible layout

Input Section
Upload a .csv file or enter student data manually

Click Submit to process data

Output Section
Table showing student marks and grades

Summary statistics (average, top, bottom)

Charts for better understanding

Buttons to clear input or start over

Functionality Details
Input Methods
CSV Upload: Requires two columns - Name and Marks

Manual Form: Add individual student entries one at a time

Grade Logic
Grades are assigned based on the following criteria:

A: 90 and above

B: 75 to 89

C: 50 to 74

F: Below 50

Chart Generation
Bar Chart: Student names vs marks

Pie Chart: Grade distribution percentages

Tools and Controls
Clear: Resets all data and views

Reload: Returns to the input screen for new data

User Interface and Design
Markviz is styled using TailwindCSS for a modern, responsive interface. Features include:

Mobile-friendly layout

Minimalist design for clarity

Smooth user interactions with rounded edges and spacing

Best Practices
Ensure your CSV is correctly formatted with "Name" and "Marks" headers

Avoid submitting incomplete data

Use a modern browser for best performance

Always review results before exporting or saving

Use Cases
Teachers preparing academic reports

Students analyzing personal results

Institutions comparing class performance

Developers or researchers analyzing educational data

Conclusion
Markviz is more than a marks calculator — it’s an intelligent student performance analyzer. With flexible input, automatic grading, and rich visual feedback, it helps users make informed decisions and understand academic trends at a glance.
