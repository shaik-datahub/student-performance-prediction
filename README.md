# Student Performance Prediction in Online Courses Using ML Algorithms

This repository contains an end-to-end Machine Learning and Data Science project titled **"Students Performance Prediction in Online Courses Using Machine Learning Algorithms"** using Python. 

The project is inspired by and dedicated to the Internship Completion Certificate of **SHAIK MAHABOOB BASHA**, a student of **BSC(Data Science)** at **SRI SAI CHAITANYA DEGREE COLLEGE, GIDDALUR**, who completed his internship program at **Pooja Soft Solutions, Ongole** (from 10th January, 2024 to 30th March, 2024).

---

## 🚀 Key Features

1. **Synthetic Data Engine (`generate_data.py`)**: Automatically generates a highly realistic synthetic dataset of 1,200 student records featuring study hours, attendance, previous grades, discussion board posts, quizzes completed, and average quiz scores.
2. **Predictive AI Pipeline (`train_model.py`)**: Trains, evaluates, and exports a Random Forest Classifier to predict student outcomes into three categories: **At Risk (Fail)**, **On Track (Pass)**, and **Excelling (Excel)**.
3. **Premium Streamlit UI/UX (`app.py`)**:
   - **Modern Aesthetic**: Glassmorphism layouts, glowing gradients, subtle dark mode background, and customized typography.
   - **Interactive EDA Dashboard**: Data visualization using Plotly (e.g. interactive scatter plots, feature importances, pie charts, and group boxplots).
   - **Dynamic Predictive Calculator**: Sliders and numerical inputs that feed features to the model for real-time predictions.
   - **Actionable AI Recommendations**: Computes specific, personalized advice (e.g., "Add 3 hours/week of study and increase attendance by 5% to reach the 'Excel' category").
   - **Digital Certificate Reproductions**: A beautifully rendered digital version of the Pooja Soft Solutions internship completion certificate.

---

## 🛠️ Project Structure

- `generate_data.py`: Creates `online_course_students.csv` synthetic dataset.
- `train_model.py`: Preprocesses data, trains the Random Forest model, and saves `student_performance_model.pkl` and `scaler.pkl`.
- `app.py`: Streamlit web dashboard codebase with custom CSS styling and Plotly graphics.
- `requirements.txt`: Python package requirements.
- `run_project.bat`: One-click batch file to install requirements and start the dashboard.
- `online_course_students.csv` (Generated): Raw data storage.
- `*.pkl` (Generated): Serialized model and scaler objects.

---

## ⚙️ Installation and Setup

### Prerequisites
Make sure you have Python 3.8+ installed on your computer.

### Easy Start (Windows)
1. Double-click `run_project.bat`. It will automatically:
   - Install all Python dependencies.
   - Generate the dataset (if missing).
   - Train and serialize the model (if missing).
   - Start the Streamlit server and open it in your default web browser.

### Manual Launch (Terminal)
Open terminal/PowerShell in this project directory and run:

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Generate dataset**:
   ```bash
   python generate_data.py
   ```
3. **Train model**:
   ```bash
   python train_model.py
   ```
4. **Run Web Application**:
   ```bash
   streamlit run app.py
   ```

Open the link shown in the terminal (usually `http://localhost:8501`) in your browser to view the application.
