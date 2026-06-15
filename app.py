import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import os

# Page Configuration
st.set_page_config(
    page_title="Student Performance AI Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dark Theme (Glassmorphism & Gradients)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

/* Main app setup */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #020617 100%);
    color: #f1f5f9;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Custom header/title styles */
.header-container {
    background: linear-gradient(90deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 30px;
    text-align: center;
}

.main-title {
    font-family: 'Outfit', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 30%, #c084fc 70%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    padding-bottom: 8px;
    letter-spacing: -0.5px;
}

.subtitle {
    font-size: 1.15rem;
    color: #94a3b8;
    margin-top: 5px;
    font-weight: 300;
}

/* Glassmorphism Cards */
.glass-card {
    background: rgba(30, 41, 59, 0.45);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.25);
    margin-bottom: 25px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
    border-color: rgba(129, 140, 248, 0.3);
    box-shadow: 0 12px 35px 0 rgba(99, 102, 241, 0.15);
}

.card-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #38bdf8;
    margin-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 8px;
}

/* Custom Badges */
.badge-fail {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.35) 100%);
    color: #fca5a5;
    padding: 8px 16px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 1.1rem;
    border: 1px solid rgba(239, 68, 68, 0.4);
    display: inline-block;
    text-align: center;
}

.badge-pass {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.35) 100%);
    color: #93c5fd;
    padding: 8px 16px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 1.1rem;
    border: 1px solid rgba(59, 130, 246, 0.4);
    display: inline-block;
    text-align: center;
}

.badge-excel {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.25) 0%, rgba(147, 51, 234, 0.4) 100%);
    color: #e9d5ff;
    padding: 8px 24px;
    border-radius: 9999px;
    font-weight: 800;
    font-size: 1.2rem;
    border: 1px solid rgba(168, 85, 247, 0.5);
    display: inline-block;
    animation: pulse 2s infinite;
    text-align: center;
    box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}

/* Metrics styles */
.metric-val {
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
}
.metric-lbl {
    font-size: 0.9rem;
    color: #94a3b8;
}

/* Certificate display */
.cert-frame {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 8px double #d97706;
    border-radius: 12px;
    padding: 40px;
    max-width: 800px;
    margin: 0 auto;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    color: #f8fafc;
    position: relative;
}

.cert-header {
    text-align: center;
    color: #fbbf24;
    font-family: 'Outfit', serif;
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 5px;
}

.cert-sub {
    text-align: center;
    font-size: 0.9rem;
    letter-spacing: 2px;
    color: #94a3b8;
    text-transform: uppercase;
    margin-bottom: 30px;
    border-bottom: 2px solid rgba(251, 191, 36, 0.3);
    padding-bottom: 10px;
}

.cert-body {
    font-size: 1.15rem;
    line-height: 1.8;
    text-align: justify;
    margin-bottom: 40px;
}

.cert-sign {
    margin-top: 50px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}

.signature-line {
    border-top: 1px solid #94a3b8;
    width: 200px;
    text-align: center;
    padding-top: 5px;
    font-size: 0.9rem;
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# Helper function to load dataset
@st.cache_data
def load_dataset():
    if os.path.exists('online_course_students.csv'):
        return pd.read_csv('online_course_students.csv')
    return None

# Load model and scaler
@st.cache_resource
def load_ml_assets():
    model_path = 'student_performance_model.pkl'
    scaler_path = 'scaler.pkl'
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        return None, None
    with open(model_path, 'rb') as mf:
        model = pickle.load(mf)
    with open(scaler_path, 'rb') as sf:
        scaler = pickle.load(sf)
    return model, scaler

df = load_dataset()
rf_model, scaler = load_ml_assets()

# Sidebar Navigation
st.sidebar.markdown("<h2 style='text-align:center; font-family: Outfit, sans-serif; color:#38bdf8;'>🎓 CourseAI</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='margin:10px 0; opacity:0.15;'>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation Menu",
    ["📊 Dashboard & Insights", "🔮 AI Prediction Calculator", "🏆 Internship Certificate Details"],
    index=1
)

st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:10px; font-size:0.85rem;'>
<span style='color:#a855f7; font-weight:bold;'>Project Context:</span><br>
Students Performance Prediction in Online Courses using ML algorithms.
<br><br>
<span style='color:#38bdf8;'>Developed by:</span><br>
Shaik Mahaboob Basha (BSC Data Science)
</div>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header-container">
    <div class="main-title">Students Performance Prediction</div>
    <div class="subtitle">Interactive ML Analytics & Performance Forecaster for Online Education</div>
</div>
""", unsafe_allow_html=True)

# If assets are not trained, guide the user
if rf_model is None or df is None:
    st.warning("⚠️ Machine Learning assets not found. Please click below to generate the synthetic student dataset and train the model.")
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🚀 Train Model Now", use_container_width=True):
            with st.spinner("Generating dataset and training Random Forest model..."):
                import generate_data
                import train_model
                generate_data.generate_student_data()
                train_model.train_and_save_model()
            st.success("🎉 Dataset and ML Model successfully generated and trained! Reloading page...")
            st.rerun()
    st.stop()


# -------------------------------- PAGE 1: DASHBOARD & INSIGHTS --------------------------------
if page == "📊 Dashboard & Insights":
    st.subheader("Interactive Exploratory Data Analysis & Feature Impact")
    
    # Key stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <div class="metric-lbl">TOTAL STUDENTS ANALYZED</div>
            <div class="metric-val">{}</div>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    with col2:
        pass_rate = (len(df[df['final_grade'] >= 1]) / len(df)) * 100
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <div class="metric-lbl">OVERALL SUCCESS RATE (PASS/EXCEL)</div>
            <div class="metric-val">{:.1f}%</div>
        </div>
        """.format(pass_rate), unsafe_allow_html=True)
    with col3:
        avg_study = df['study_hours_per_week'].mean()
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <div class="metric-lbl">AVG STUDY HOURS / WEEK</div>
            <div class="metric-val">{:.1f} hrs</div>
        </div>
        """.format(avg_study), unsafe_allow_html=True)
    with col4:
        avg_quiz = df['average_quiz_score'].mean()
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <div class="metric-lbl">AVG QUIZ SCORE</div>
            <div class="metric-val">{:.1f}%</div>
        </div>
        """.format(avg_quiz), unsafe_allow_html=True)

    # Visualization Row 1
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Study Hours vs. Average Quiz Scores</div>', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df, 
            x="study_hours_per_week", 
            y="average_quiz_score",
            color=df['final_grade'].map({0: 'Fail', 1: 'Pass', 2: 'Excel'}),
            color_discrete_map={'Fail': '#ef4444', 'Pass': '#3b82f6', 'Excel': '#a855f7'},
            labels={'study_hours_per_week': 'Weekly Study Hours', 'average_quiz_score': 'Avg Quiz Score (%)', 'color': 'Performance'},
            opacity=0.75,
            template="plotly_dark"
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_v2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Feature Importance (Random Forest Classifier)</div>', unsafe_allow_html=True)
        # Calculate feature importances
        features = [
            'study_hours_per_week', 'attendance_rate', 'discussion_posts', 
            'quizzes_completed', 'average_quiz_score', 'previous_grade', 'completed_projects'
        ]
        importances = rf_model.feature_importances_
        feat_df = pd.DataFrame({
            'Feature': [f.replace('_', ' ').title() for f in features],
            'Importance': importances
        }).sort_values('Importance', ascending=True)
        
        fig_bar = px.bar(
            feat_df,
            x='Importance',
            y='Feature',
            orientation='h',
            template="plotly_dark",
            color='Importance',
            color_continuous_scale=['#312e81', '#6366f1', '#a855f7']
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=10, b=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Visualization Row 2
    col_v3, col_v4 = st.columns(2)
    
    with col_v3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Performance Grade Distribution</div>', unsafe_allow_html=True)
        grade_counts = df['final_grade'].map({0: 'Fail', 1: 'Pass', 2: 'Excel'}).value_counts().reset_index()
        grade_counts.columns = ['Performance', 'Students Count']
        fig_pie = px.pie(
            grade_counts,
            values='Students Count',
            names='Performance',
            hole=0.45,
            color='Performance',
            color_discrete_map={'Fail': '#ef4444', 'Pass': '#3b82f6', 'Excel': '#a855f7'},
            template="plotly_dark"
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_v4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Attendance vs Completed Projects</div>', unsafe_allow_html=True)
        fig_box = px.box(
            df,
            x="completed_projects",
            y="attendance_rate",
            color=df['final_grade'].map({0: 'Fail', 1: 'Pass', 2: 'Excel'}),
            color_discrete_map={'Fail': '#ef4444', 'Pass': '#3b82f6', 'Excel': '#a855f7'},
            labels={'completed_projects': 'Completed Projects', 'attendance_rate': 'Attendance Rate (%)', 'color': 'Performance'},
            template="plotly_dark"
        )
        fig_box.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=10, b=20),
            boxmode='group'
        )
        st.plotly_chart(fig_box, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ------------------------- PAGE 2: AI PREDICTION CALCULATOR -------------------------
elif page == "🔮 AI Prediction Calculator":
    st.subheader("Predict Live Student Outcomes using Machine Learning")
    
    col_input, col_result = st.columns([5, 6])
    
    with col_input:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">⚙️ Student Parameters Input</div>', unsafe_allow_html=True)
        
        # Interactive Inputs
        study_hours = st.slider("Weekly Study Hours", 1.0, 30.0, 12.0, 0.5, help="Average number of hours the student studies per week")
        attendance = st.slider("Session Attendance Rate (%)", 0.0, 100.0, 75.0, 1.0, help="Live online class attendance percentage")
        quiz_score = st.slider("Average Quiz Score (%)", 0.0, 100.0, 68.0, 1.0, help="Average score across online course quizzes")
        
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            disc_posts = st.number_input("Forum Discussion Posts", 0, 150, 15, step=1, help="Total student forum posts/replies")
            quizzes_comp = st.number_input("Quizzes Completed", 0, 10, 8, step=1, help="Total number of quizzes completed")
        with col_in2:
            prev_gpa = st.number_input("Previous GPA (out of 4.0)", 1.0, 4.0, 2.8, step=0.1, help="Student's Cumulative Grade Point Average")
            projects = st.number_input("Completed Projects", 0, 5, 2, step=1, help="Course projects completed (0-5)")
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🔍 Predictive AI Analysis</div>', unsafe_allow_html=True)
        
        # Assemble feature array
        input_data = pd.DataFrame([[
            study_hours, attendance, disc_posts, quizzes_comp, quiz_score, prev_gpa, projects
        ]], columns=[
            'study_hours_per_week', 'attendance_rate', 'discussion_posts', 
            'quizzes_completed', 'average_quiz_score', 'previous_grade', 'completed_projects'
        ])
        
        # Scale input
        input_scaled = scaler.transform(input_data)
        
        # Predict Class and Probability
        prediction = rf_model.predict(input_scaled)[0]
        probabilities = rf_model.predict_proba(input_scaled)[0]
        
        # Display Results
        col_badge, col_prob = st.columns([1, 1])
        
        with col_badge:
            st.markdown("<p style='font-size:0.9rem; color:#94a3b8; margin-bottom:5px;'>PREDICTED PERFORMANCE</p>", unsafe_allow_html=True)
            if prediction == 0:
                st.markdown("<div class='badge-fail'>⚠️ AT RISK (FAIL)</div>", unsafe_allow_html=True)
            elif prediction == 1:
                st.markdown("<div class='badge-pass'>✅ ON TRACK (PASS)</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='badge-excel'>✨ EXCELLING (EXCEL)</div>", unsafe_allow_html=True)
                
        with col_prob:
            conf = probabilities[prediction] * 100
            st.markdown("<p style='font-size:0.9rem; color:#94a3b8; margin-bottom:5px;'>PREDICTION CONFIDENCE</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:2rem; font-weight:800; color:#ffffff; margin:0;'>{conf:.1f}%</p>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Probability Breakdown Plotly Chart
        categories = ['Fail', 'Pass', 'Excel']
        fig_prob = go.Figure(go.Bar(
            x=probabilities * 100,
            y=categories,
            orientation='h',
            marker=dict(
                color=['#ef4444', '#3b82f6', '#a855f7'],
                line=dict(color='rgba(255,255,255,0.1)', width=1)
            )
        ))
        
        fig_prob.update_layout(
            title=dict(text="Probability Distribution (%)", font=dict(color="#94a3b8", size=12)),
            xaxis=dict(range=[0, 100], gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color="#94a3b8")),
            yaxis=dict(tickfont=dict(color="#f1f5f9")),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=200,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_prob, use_container_width=True)
        
        # Actionable AI Coaching Insights
        st.markdown("<div style='border-top:1px solid rgba(255,255,255,0.08); padding-top:15px; margin-top:10px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#38bdf8; font-family:Outfit; margin-bottom:10px;'>💡 AI Recommendations & Interventions</h4>", unsafe_allow_html=True)
        
        # Compute difference from successful students (Pass or Excel averages)
        success_students = df[df['final_grade'] == 2]
        avg_success_hours = success_students['study_hours_per_week'].mean()
        avg_success_attendance = success_students['attendance_rate'].mean()
        avg_success_quizzes = success_students['average_quiz_score'].mean()
        
        recommendations = []
        
        if prediction == 0: # Fail
            recommendations.append(f"🔴 **Urgent Intervention Needed**: The student's stats indicate they are at risk of failing the course.")
            if study_hours < avg_success_hours:
                diff = avg_success_hours - study_hours
                recommendations.append(f"⏱️ **Increase Study Time**: Guide the student to study an extra **{diff:.1f} hours/week** to match top-tier student levels.")
            if attendance < avg_success_attendance:
                diff = avg_success_attendance - attendance
                recommendations.append(f"📅 **Improve Attendance**: Recommend improving session attendance rate by **{diff:.1f}%** to build strong concept foundations.")
            if quiz_score < avg_success_quizzes:
                diff = avg_success_quizzes - quiz_score
                recommendations.append(f"✏️ **Quiz Improvement**: Encourage revision and scoring higher on subsequent quizzes. Target improvement: **+{diff:.1f}%** average score.")
        
        elif prediction == 1: # Pass
            recommendations.append(f"🟡 **Steady Progress**: The student is on track to pass, but can easily push to the 'Excel' category with a few adjustments.")
            if study_hours < avg_success_hours:
                diff = avg_success_hours - study_hours
                recommendations.append(f"🚀 **Study Hours Boost**: Adding **{diff:.1f} hours/week** of study can boost performance to excellent grade ranges.")
            if quiz_score < avg_success_quizzes:
                diff = avg_success_quizzes - quiz_score
                recommendations.append(f"🎯 **Aim Higher in Quizzes**: Scoring just **{diff:.1f}%** higher on average in quizzes will strengthen concepts for the final grade.")
                
        else: # Excel
            recommendations.append(f"🟢 **Superb Performance**: The student is performing beautifully and is highly likely to excel!")
            recommendations.append("🌟 **Maintain Momentum**: Encourage maintaining this level of participation. Consider assigning mentorship roles or advanced project tracks.")
            
        for rec in recommendations:
            st.markdown(rec)
            
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ------------------------- PAGE 3: INTERNSHIP DETAILS -------------------------
elif page == "🏆 Internship Certificate Details":
    st.subheader("Certified Internship Program Accomplishment")
    
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 30px;">
        <div class="card-title">🎓 Student and Internship Verification</div>
        <p>This interactive project dashboard is built based on the authenticated Certificate of Internship Completion issued by <b>Pooja Soft Solutions</b>.</p>
    </div>
    """, unsafe_allow_html=True)

    # Digitally Rendered Certificate
    st.markdown("""
    <div class="cert-frame">
        <div class="cert-header">POOJA SOFT SOLUTIONS</div>
        <div class="cert-sub">AN ISO 9001:2015 CERTIFIED INSTITUTION</div>
        <div style="text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: -20px; margin-bottom: 25px;">
            Regd. No: AP-08-44-009-03451558 | <a href="http://www.poojacomputereducation.com" target="_blank" style="color: #fbbf24; text-decoration: none;">www.poojacomputereducation.com</a>
        </div>
        
        <div style="text-align: right; color: #94a3b8; font-size: 0.9rem; margin-bottom: 30px;">
            <b>Date:</b> 30/03/2024
        </div>
        
        <div style="text-align: center; font-family: 'Outfit', sans-serif; font-size: 1.5rem; font-weight: 600; color: #e2e8f0; margin-bottom: 20px; letter-spacing: 1px;">
            TO WHOM SO EVER IT MAY CONCERN
        </div>
        
        <div style="text-align: center; font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 700; color: #fbbf24; margin-bottom: 30px; letter-spacing: 1px;">
            CERTIFICATION OF INTERNSHIP COMPLETION
        </div>
        
        <div class="cert-body">
            This is to certify that <b>SHAIK MAHABOOB BASHA</b>, studying <b>BSC(Data Science)</b>, Hall Ticket No: <b>Y213263031</b>, in <b>SRI SAI CHAITANYA DEGREE COLLEGE, GIDDALUR</b>, has done his Internship Program, on Work Entitled <b>"Students Performance Prediction in Online Courses Using Machine Learning Algorithms"</b> using <b>Python</b> in Pooja Soft Solutions, Ongole from <b>10<sup>th</sup> January, 2024 to 30<sup>th</sup> March, 2024</b> in partial fulfillment for the award of the certificate from the degree mentioned above and this report of the project work carried out under our guidance. The student displayed analytical capability, has innovative approach to solve problem and has produced good results.
            <br><br>
            We wish the very best for his career and future endeavors.
        </div>
        
        <div class="cert-sign">
            <div>
                <p style="font-size:0.85rem; color:#64748b; margin-bottom:0;">Location:</p>
                <p style="font-weight:600; margin-top:0;">Ongole, AP, India</p>
            </div>
            <div class="signature-line">
                <span style="font-family: 'Dancing Script', cursive; font-size: 1.1rem; color: #fbbf24; display:block; margin-bottom:2px;">Manager - Training & Project</span>
                <b>For Pooja Soft Solutions</b><br>
                Manager
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
