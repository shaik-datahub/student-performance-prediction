import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_and_save_model():
    dataset_path = 'online_course_students.csv'
    if not os.path.exists(dataset_path):
        print("Dataset not found! Running generate_data.py first...")
        import generate_data
        generate_data.generate_student_data()
        
    # Load dataset
    df = pd.read_csv(dataset_path)
    
    # Define features and target
    features = [
        'study_hours_per_week',
        'attendance_rate',
        'discussion_posts',
        'quizzes_completed',
        'average_quiz_score',
        'previous_grade',
        'completed_projects'
    ]
    target = 'final_grade'
    
    X = df[features]
    y = df[target]
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest Classifier
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    
    # Predict and evaluate
    y_pred = rf_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n--- Model Evaluation Results ---")
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Fail', 'Pass', 'Excel']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Print Feature Importances
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("\nFeature Importances:")
    for f in range(X.shape[1]):
        print(f"{f + 1}. {features[indices[f]]} ({importances[indices[f]]:.4f})")
        
    # Save the model and scaler
    model_filename = 'student_performance_model.pkl'
    scaler_filename = 'scaler.pkl'
    
    with open(model_filename, 'wb') as model_file:
        pickle.dump(rf_model, model_file)
    with open(scaler_filename, 'wb') as scaler_file:
        pickle.dump(scaler, scaler_file)
        
    print(f"\nModel and Scaler successfully saved!")
    print(f"Model saved to: {os.path.abspath(model_filename)}")
    print(f"Scaler saved to: {os.path.abspath(scaler_filename)}")

if __name__ == '__main__':
    train_and_save_model()
