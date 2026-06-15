@echo off
echo ==========================================================
echo       Student Performance Prediction AI Dashboard Setup
echo ==========================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo.
echo [1/4] Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] There was an issue installing dependencies. Attempting individual install...
    pip install pandas numpy scikit-learn streamlit plotly matplotlib
)

echo.
echo [2/4] Generating student dataset...
if not exist online_course_students.csv (
    python generate_data.py
) else (
    echo online_course_students.csv already exists. Skipping...
)

echo.
echo [3/4] Training Random Forest model...
if not exist student_performance_model.pkl (
    python train_model.py
) else (
    echo student_performance_model.pkl already exists. Skipping...
)

echo.
echo [4/4] Starting Streamlit application...
echo Streamlit dashboard will open automatically in your browser.
echo.
streamlit run app.py

pause
