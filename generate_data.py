import pandas as pd
import numpy as np
import os

def generate_student_data(num_students=1200, seed=42):
    np.random.seed(seed)
    
    # Generate features
    study_hours = np.random.uniform(2, 28, num_students)  # Hours per week
    attendance = np.random.uniform(40, 100, num_students)   # Attendance rate %
    discussion_posts = np.random.randint(2, 95, num_students) # Forum posts
    quizzes_completed = np.random.randint(3, 11, num_students) # 0 to 10 quizzes
    
    # Quiz scores correlated with study hours and attendance
    quiz_noise = np.random.normal(0, 10, num_students)
    average_quiz_score = (study_hours * 1.5 + attendance * 0.5 + quiz_noise)
    average_quiz_score = np.clip(average_quiz_score, 10, 100)
    
    # Previous GPA (1.5 to 4.0)
    previous_grade = np.random.uniform(1.8, 4.0, num_students)
    
    # Projects completed (depends on attendance and study hours)
    project_prob = np.clip((attendance / 100.0) * (study_hours / 20.0), 0.1, 1.0)
    completed_projects = np.array([np.random.binomial(5, p) for p in project_prob])
    
    # Calculate performance score to define target variable
    # Scale features to 0-1
    s_hours_scaled = study_hours / 28.0
    attendance_scaled = attendance / 100.0
    disc_posts_scaled = discussion_posts / 95.0
    quizzes_scaled = quizzes_completed / 10.0
    quiz_score_scaled = average_quiz_score / 100.0
    prev_grade_scaled = (previous_grade - 1.8) / (4.0 - 1.8)
    projects_scaled = completed_projects / 5.0
    
    performance_score = (
        0.25 * s_hours_scaled +
        0.20 * attendance_scaled +
        0.15 * disc_posts_scaled +
        0.10 * quizzes_scaled +
        0.15 * quiz_score_scaled +
        0.10 * prev_grade_scaled +
        0.05 * projects_scaled
    )
    
    # Add noise to performance score
    performance_score += np.random.normal(0, 0.06, num_students)
    performance_score = np.clip(performance_score, 0, 1)
    
    # Classify final grade: 0 = Fail, 1 = Pass, 2 = Excel
    final_grade = []
    for score in performance_score:
        if score < 0.42:
            final_grade.append(0) # Fail
        elif score < 0.72:
            final_grade.append(1) # Pass
        else:
            final_grade.append(2) # Excel
            
    # Create DataFrame
    df = pd.DataFrame({
        'student_id': [f"STU{1000+i}" for i in range(num_students)],
        'study_hours_per_week': np.round(study_hours, 1),
        'attendance_rate': np.round(attendance, 1),
        'discussion_posts': discussion_posts,
        'quizzes_completed': quizzes_completed,
        'average_quiz_score': np.round(average_quiz_score, 1),
        'previous_grade': np.round(previous_grade, 2),
        'completed_projects': completed_projects,
        'performance_score': np.round(performance_score, 3),
        'final_grade': final_grade
    })
    
    # Save to CSV
    output_path = 'online_course_students.csv'
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully created with {num_students} rows!")
    print(f"Saved to {os.path.abspath(output_path)}")
    print(df['final_grade'].value_counts())

if __name__ == '__main__':
    generate_student_data()
