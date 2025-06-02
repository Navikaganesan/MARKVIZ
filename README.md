# Markviz: Student Marks Analyzer & Visualizer

Welcome to **Markviz** — a lightweight, web-based application for analyzing and visualizing student marks. Built using Flask and powered by `matplotlib`, Markviz turns raw score data into meaningful insights through clear tables and charts.

 Markviz is designed to be simple, effective, and educational — ideal for teachers, students, and data enthusiasts alike.

---

## The Markviz Advantage

While traditional mark management tools require manual calculation or complicated software, Markviz streamlines the process:

- Upload a CSV or enter marks manually
- Instantly generate grade distributions
- Visualize student performance using charts

This makes Markviz ideal for:

- Teachers preparing class reports
- Students reviewing academic progress
- Educational institutions conducting analytics
- Developers prototyping educational tools

---

## Key Features

- **CSV & Manual Entry**: Upload `.csv` files or input student names and marks directly via form.
- **Automated Grading**: Assigns grades based on thresholds (A, B, C, F).
- **Statistical Summary**: Computes class average, top and bottom scores.
- **Chart Visualization**: Displays bar charts and pie charts of performance and grade distribution.
- **Clean UI**: Responsive interface styled using TailwindCSS.
- **Download & Reset Tools**: Clear results or re-analyze new datasets with ease.

---

## Interface Overview

### Header
- App title: Markviz
- Upload toggle: Switch between CSV and Manual Input

### Input Section
- **CSV Upload**: Requires `Name` and `Marks` columns
- **Manual Input**: Add each student record individually

### Output Section
- Tabular summary of marks and grades
- Statistics: Average, Highest, Lowest
- Charts: Bar chart (marks) and Pie chart (grades)
- Controls: Clear, Submit, Reset

---

## Grading Logic

Grades are computed using this scale:

- **A+**: 90 and above
- **A**:  75 and above
- **B**:  60 and above 
- **C**:  50 and above
- **D**:  35 and above 
- **F(Fail)**: Below 35

---

## Visualizations

Charts are rendered with `matplotlib`:

- **Bar Chart**: Compares marks across all students
- **Pie Chart**: Shows percentage distribution of grades

These provide immediate insight into student performance trends.

---

## Tips for Best Results

- Ensure CSV format is clean and contains two columns: `Name`, `Marks`
- Avoid empty or malformed entries
- Use a modern browser for full compatibility
- Always double-check auto-generated results

---

## Use Cases

- Generate class performance reports quickly
- Track and compare semester-wise progress
- Automate grading and visualization for small institutions
- Learn data visualization using educational datasets

---

## Conclusion

**Markviz** is more than a marks calculator — it's a smart analysis and visualization tool built for clarity and speed. Whether you're an educator, a student, or a hobbyist, Markviz brings you the insights you need in just a few clicks.

---

**Happy Analyzing.**
