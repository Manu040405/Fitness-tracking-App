import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import warnings
import base64
import random
import uuid
import time

warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="Enhanced Fitness Tracker",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved appearance with modern theme and glassy effects
def local_css():
    st.markdown("""
        <style>
        /* Global styling */
        .main .block-container {
            padding-top: 2rem;
        }
        
        /* Custom theme colors - vibrant interactive palette */
        :root {
            --primary-color: #8e44ad;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --background-color: #f8f9fa;
            --text-color: #2c3e50;
            --light-text: #7f8c8d;
            --success-color: #2ecc71;
            --warning-color: #f39c12;
            --glass-bg: rgba(255, 255, 255, 0.25);
            --glass-border: rgba(255, 255, 255, 0.18);
            --glass-highlight: rgba(255, 255, 255, 0.6);
            --glass-shadow: rgba(0, 0, 0, 0.1);
        }
        
        /* Streamlit component styling */
        .stMetric {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px !important;
            border: 1px solid var(--glass-border);
            box-shadow: 0 8px 32px var(--glass-shadow);
            transition: all 0.4s ease;
        }
        .stMetric:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px var(--glass-shadow);
            border-color: var(--glass-highlight);
        }
        .stMetric label {
            color: var(--text-color) !important;
            font-weight: 500 !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        .stMetric [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: bold !important;
            color: var(--primary-color) !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Custom components */
        .badge {
            display: inline-block;
            padding: 8px 15px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 25px;
            color: white;
            font-weight: bold;
            margin: 5px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .badge:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 10px 25px rgba(0,0,0,0.25);
        }
        
        .workout-card {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 18px;
            box-shadow: 0 8px 32px var(--glass-shadow);
            transition: all 0.4s ease;
            border-left: 4px solid var(--primary-color);
            border: 1px solid var(--glass-border);
        }
        .workout-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 35px var(--glass-shadow);
            border-color: var(--glass-highlight);
        }
        
        .challenge-card {
            background: linear-gradient(135deg, 
                          rgba(142, 68, 173, 0.8), 
                          rgba(52, 152, 219, 0.8));
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            color: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .challenge-card:hover {
            transform: translateY(-8px) scale(1.03);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        
        .achievement-icon {
            font-size: 32px;
            margin-right: 15px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .progress-container {
            width: 100%;
            background: rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-radius: 20px;
            margin: 15px 0;
            overflow: hidden;
            height: 25px;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            border-radius: 20px;
            transition: width 1s cubic-bezier(0.19, 1, 0.22, 1);
            text-align: center;
            color: white;
            font-weight: bold;
            line-height: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
        
        /* Animation effects */
        .tab-content {
            animation: fadeIn 0.8s cubic-bezier(0.19, 1, 0.22, 1);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(142, 68, 173, 0.7); }
            70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(142, 68, 173, 0); }
            100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(142, 68, 173, 0); }
        }
        
        /* Login/Register form styling with glassy effect */
        .auth-container {
            max-width: 450px;
            margin: 3rem auto;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.18);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .auth-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, 
                             rgba(255, 255, 255, 0.1) 0%, 
                             rgba(255, 255, 255, 0.05) 30%, 
                             transparent 70%);
            z-index: -1;
        }
        
        .auth-header {
            margin-bottom: 30px;
            color: var(--primary-color);
            font-size: 28px;
            font-weight: bold;
            text-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .auth-input {
            width: 100%;
            padding: 15px 20px;
            margin-bottom: 20px;
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            font-size: 16px;
            color: var(--text-color);
            transition: all 0.4s ease;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        .auth-input:focus {
            background: rgba(255, 255, 255, 0.25);
            border-color: rgba(255, 255, 255, 0.4);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            outline: none;
        }
        
        .auth-input::placeholder {
            color: rgba(44, 62, 80, 0.6);
        }
        
        .auth-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
            text-shadow: 0 1px 3px rgba(0,0,0,0.2);
            margin-top: 10px;
        }
        
        .auth-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 25px rgba(0,0,0,0.2);
            animation: pulse 1.5s infinite;
        }
        
        .auth-switch {
            margin-top: 20px;
            color: var(--text-color);
            font-size: 15px;
        }
        
        .auth-switch a {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .auth-switch a:hover {
            text-decoration: underline;
            color: var(--secondary-color);
        }
        
        /* Avatar styling */
        .user-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 12px;
            font-size: 18px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            border: 2px solid rgba(255, 255, 255, 0.3);
            text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        }
        
        /* Custom styling for buttons */
        button[data-testid="baseButton-secondary"] {
            background: rgba(255, 255, 255, 0.3) !important;
            backdrop-filter: blur(5px) !important;
            -webkit-backdrop-filter: blur(5px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1) !important;
            transition: all 0.3s !important;
        }
        
        button[data-testid="baseButton-secondary"]:hover {
            background: rgba(255, 255, 255, 0.4) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(0,0,0,0.15) !important;
        }
        
        button[data-testid="baseButton-primary"] {
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color)) !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
            transition: all 0.3s !important;
        }
        
        button[data-testid="baseButton-primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
        }
        
        /* Form inputs styling */
        div[data-baseweb="input"] input, 
        div[data-baseweb="textarea"] textarea,
        div[data-baseweb="select"] div {
            background: rgba(255, 255, 255, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 10px !important;
            transition: all 0.3s !important;
        }
        
        div[data-baseweb="input"] input:focus,
        div[data-baseweb="textarea"] textarea:focus,
        div[data-baseweb="select"] div:focus-within {
            background: rgba(255, 255, 255, 0.3) !important;
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(142, 68, 173, 0.2) !important;
        }
        
        /* Body background gradient for added effect */
        body {
            background: linear-gradient(135deg, #f5f7fa, #e8edf2);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            background: rgba(255, 255, 255, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(to bottom, var(--primary-color), var(--secondary-color));
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# Initialize Session State
if 'workout_history' not in st.session_state:
    st.session_state.workout_history = []
if 'goals' not in st.session_state:
    st.session_state.goals = {'weekly_calories': 2000, 'weekly_duration': 150}
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = {
        'Beginner': ['Walking (30 min)', 'Light stretching (15 min)', 'Yoga (20 min)', 'Gentle cycling (20 min)'],
        'Intermediate': ['Jogging (30 min)', 'Cycling (45 min)', 'Swimming (30 min)', 'Bodyweight exercises (20 min)'],
        'Advanced': ['HIIT (30 min)', 'Weight Training (45 min)', 'Running (5k)', 'Circuit training (40 min)']
    }
if 'achievements' not in st.session_state:
    st.session_state.achievements = {
        'first_workout': {'earned': False, 'name': 'First Step', 'icon': '🎯', 'description': 'Log your first workout'},
        'three_workouts': {'earned': False, 'name': 'Getting Started', 'icon': '🔥', 'description': 'Complete 3 workouts'},
        'consistency': {'earned': False, 'name': 'Consistency King', 'icon': '👑', 'description': 'Work out 3 days in a row'},
        'calorie_milestone': {'earned': False, 'name': 'Calorie Crusher', 'icon': '💪', 'description': 'Burn 500 total calories'},
        'different_workouts': {'earned': False, 'name': 'Variety Pack', 'icon': '🌈', 'description': 'Try 3 different workout types'}
    }
if 'weight_tracker' not in st.session_state:
    st.session_state.weight_tracker = []
if 'step_tracker' not in st.session_state:
    st.session_state.step_tracker = []
if 'challenges' not in st.session_state:
    st.session_state.challenges = [
        {'id': 1, 'name': '7-Day Streak', 'description': 'Complete 7 workouts in 7 days', 'reward': '🏆 Gold Badge', 'completed': False},
        {'id': 2, 'name': 'Cardio Master', 'description': 'Complete 5 cardio workouts', 'reward': '🏅 Silver Badge', 'completed': False},
        {'id': 3, 'name': '1000 Calorie Burn', 'description': 'Burn a total of 1000 calories', 'reward': '🔥 Fire Badge', 'completed': False}
    ]
if 'user_stats' not in st.session_state:
    st.session_state.user_stats = {
        'total_workouts': 0,
        'total_calories': 0,
        'total_duration': 0,
        'streak': 0,
        'last_workout_date': None
    }

# User authentication system
if 'users' not in st.session_state:
    st.session_state.users = {
        'demo@example.com': {
            'password': 'password123',
            'name': 'Demo User',
            'profile_pic': '👤'
        },
        'john@example.com': {
            'password': 'test123',
            'name': 'John Smith',
            'profile_pic': '🧑'
        },
        'jane@example.com': {
            'password': 'test123',
            'name': 'Jane Doe',
            'profile_pic': '👩'
        }
    }

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
    
if 'login_error' not in st.session_state:
    st.session_state.login_error = False

# Login page handling
def login_user(email, password):
    if email in st.session_state.users and st.session_state.users[email]['password'] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = {
            'email': email,
            'name': st.session_state.users[email]['name'],
            'profile_pic': st.session_state.users[email]['profile_pic']
        }
        st.session_state.login_error = False
        return True
    else:
        st.session_state.login_error = True
        return False

def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None

# Registration function
def register_user(name, email, password):
    if email in st.session_state.users:
        return False, "Email already registered"
    
    # Generate profile pic from first letter of name
    profile_pic = '👤'
    if name:
        initials = name[0].upper()
        avatar_options = {'A': '🧑', 'B': '👨', 'C': '👩', 'D': '👱', 'E': '👧', 
                         'F': '👦', 'G': '👨‍🦰', 'H': '👱‍♀️', 'I': '👨‍🦱', 'J': '👩‍🦱',
                         'K': '👩‍🦰', 'L': '👴', 'M': '👵', 'N': '👲', 'O': '👳‍♂️',
                         'P': '🧓', 'Q': '🧔', 'R': '👮', 'S': '👷', 'T': '💂',
                         'U': '🕵️', 'V': '👨‍⚕️', 'W': '👩‍⚕️', 'X': '🧙‍♂️', 'Y': '🧝‍♀️', 'Z': '🦸‍♂️'}
        if initials in avatar_options:
            profile_pic = avatar_options[initials]
    
    # Add user to database
    st.session_state.users[email] = {
        'password': password,
        'name': name,
        'profile_pic': profile_pic
    }
    
    # Automatically log in the new user
    login_user(email, password)
    return True, "Registration successful!"

# Check if user is logged in
if not st.session_state.logged_in:
    # Authentication mode state (login or register)
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = "login"
    
    # Background effects for login page
    st.markdown(
        """
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden;">
            <div style="position: absolute; width: 300px; height: 300px; top: -150px; left: -150px; 
                 background: radial-gradient(circle, rgba(142, 68, 173, 0.2) 0%, rgba(142, 68, 173, 0.1) 40%, transparent 70%);
                 border-radius: 50%;"></div>
            <div style="position: absolute; width: 500px; height: 500px; bottom: -250px; right: -250px; 
                 background: radial-gradient(circle, rgba(52, 152, 219, 0.2) 0%, rgba(52, 152, 219, 0.1) 40%, transparent 70%);
                 border-radius: 50%;"></div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Display animated fitness icons
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px; animation: fadeIn 1s ease-in-out;">
            <span style="font-size: 60px; margin: 0 15px; display: inline-block; animation: pulse 2s infinite;">🏋️</span>
            <span style="font-size: 60px; margin: 0 15px; display: inline-block; animation: pulse 2s infinite 0.5s;">🏃</span>
            <span style="font-size: 60px; margin: 0 15px; display: inline-block; animation: pulse 2s infinite 1s;">💪</span>
        </div>
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-size: 36px; color: #8e44ad; text-shadow: 0 2px 10px rgba(0,0,0,0.1);">Fitness Tracker Pro</h1>
            <p style="font-size: 18px; color: #2c3e50; margin-top: 0;">Your Personal Workout Companion</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Main auth container
    st.markdown(
        f"""
        <div class="auth-container">
            <h2 class="auth-header">{"Sign In" if st.session_state.auth_mode == "login" else "Create Account"}</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Login Form
    if st.session_state.auth_mode == "login":
        email = st.text_input("Email Address", placeholder="Enter your email", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        if st.button("Login", type="primary", use_container_width=True):
            if login_user(email, password):
                st.rerun()
            else:
                st.error("Invalid email or password. Please try again.")
        
        # Switch to registration form
        st.markdown(
            """
            <div class="auth-switch">
                Don't have an account? <a href="#" id="register-link">Sign up now</a>
            </div>
            <script>
                document.getElementById('register-link').addEventListener('click', function(e) {
                    e.preventDefault();
                    window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'register'}, '*');
                });
            </script>
            """, 
            unsafe_allow_html=True
        )
        
        # Handle switch to registration mode
        if st.button("Sign up now", key="switch_to_register"):
            st.session_state.auth_mode = "register"
            st.rerun()
    
    # Registration Form
    else:
        name = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
        email = st.text_input("Email Address", placeholder="Enter your email", key="reg_email")
        password = st.text_input("Password", type="password", placeholder="Enter a strong password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_confirm")
        
        if st.button("Create Account", type="primary", use_container_width=True):
            if not name or not email or not password:
                st.error("Please fill in all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = register_user(name, email, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        # Switch back to login form
        st.markdown(
            """
            <div class="auth-switch">
                Already have an account? <a href="#" id="login-link">Sign in</a>
            </div>
            <script>
                document.getElementById('login-link').addEventListener('click', function(e) {
                    e.preventDefault();
                    window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'login'}, '*');
                });
            </script>
            """, 
            unsafe_allow_html=True
        )
        
        # Handle switch to login mode
        if st.button("Sign in", key="switch_to_login"):
            st.session_state.auth_mode = "login"
            st.rerun()
    
    # Footer with benefits
    st.markdown(
        """
        <div style="margin-top: 50px; text-align: center;">
            <div style="display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;">
                <div style="text-align: center; max-width: 200px;">
                    <div style="font-size: 32px; margin-bottom: 10px;">📊</div>
                    <h3 style="margin: 0; color: #8e44ad;">Track Progress</h3>
                    <p style="font-size: 14px; color: #7f8c8d;">Monitor your workouts and see your improvements over time</p>
                </div>
                <div style="text-align: center; max-width: 200px;">
                    <div style="font-size: 32px; margin-bottom: 10px;">🎯</div>
                    <h3 style="margin: 0; color: #8e44ad;">Set Goals</h3>
                    <p style="font-size: 14px; color: #7f8c8d;">Create and achieve your personal fitness goals</p>
                </div>
                <div style="text-align: center; max-width: 200px;">
                    <div style="font-size: 32px; margin-bottom: 10px;">🏆</div>
                    <h3 style="margin: 0; color: #8e44ad;">Earn Rewards</h3>
                    <p style="font-size: 14px; color: #7f8c8d;">Complete challenges and earn achievement badges</p>
                </div>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Hidden button to capture clicks from JavaScript
    placeholder = st.empty()
    js_click_value = placeholder.text_input("", key="js_auth_mode_switch", label_visibility="collapsed")
    if js_click_value == "register":
        st.session_state.auth_mode = "register"
        st.rerun()
    elif js_click_value == "login":
        st.session_state.auth_mode = "login"
        st.rerun()
    
    # Hide the rest of the app when not logged in
    st.stop()

# Main Header with user profile
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏋️ Enhanced Fitness Tracker")
    st.markdown("Track your fitness journey with advanced insights and recommendations")

with col2:
    # User profile in header
    user_name = st.session_state.current_user['name']
    user_pic = st.session_state.current_user['profile_pic']
    
    # User profile with a cleaner design
    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end; align-items: center; margin-top: 20px;">
            <div style="display: flex; align-items: center;">
                <div class="user-avatar">{user_pic}</div>
                <span style="font-weight: bold;">{user_name}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Regular logout button 
    if st.button("Logout", key="logout_button", type="secondary", help="Click to logout"):
        logout_user()
        st.rerun()

# Sidebar Input
with st.sidebar:
    # User welcome message with name
    if st.session_state.current_user:
        user_name = st.session_state.current_user['name']
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px; background: var(--glass-bg); 
                       backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); padding: 15px; 
                       border-radius: 12px; border: 1px solid var(--glass-border); box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <div style="width: 45px; height: 45px; border-radius: 50%; background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
                           display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; margin-right: 12px;
                           box-shadow: 0 4px 10px rgba(0,0,0,0.15); border: 2px solid rgba(255, 255, 255, 0.3);">
                    {st.session_state.current_user['profile_pic']}
                </div>
                <div>
                    <div style="font-size: 18px; font-weight: bold; color: var(--primary-color);">Welcome, {user_name}!</div>
                    <div style="font-size: 14px; color: var(--light-text);">Ready to crush your fitness goals?</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.header("📝 Enter Your Details")
    
    # User Profile Section with tabs
    profile_tab, goals_tab = st.tabs(["Profile", "Goals"])
    
    with profile_tab:
        age = st.slider("Age", 10, 100, 30)
        bmi = st.slider("BMI", 15, 40, 20)
        duration = st.slider("Duration (min)", 0, 60, 15)
        heart_rate = st.slider("Heart Rate (bpm)", 60, 200, 80)
        body_temp = st.slider("Body Temperature (°C)", 36.0, 42.0, 38.0, 0.1)
        gender = st.radio("Gender", ("Male", "Female"))
        gender_encoded = 1 if gender == "Male" else 0
        
        st.markdown("---")
        fitness_level = st.selectbox(
            "Your Fitness Level", 
            ["Beginner", "Intermediate", "Advanced"],
            help="Select your current fitness level"
        )
    
    with goals_tab:
        st.subheader("🎯 Set Your Goals")
        st.session_state.goals['weekly_calories'] = st.number_input(
            "Weekly Calories Goal (kcal)",
            min_value=500,
            max_value=5000,
            value=st.session_state.goals['weekly_calories']
        )
        st.session_state.goals['weekly_duration'] = st.number_input(
            "Weekly Exercise Duration Goal (minutes)",
            min_value=30,
            max_value=500,
            value=st.session_state.goals['weekly_duration']
        )
        
        # Additional goals
        if 'steps_goal' not in st.session_state.goals:
            st.session_state.goals['steps_goal'] = 10000
        
        st.session_state.goals['steps_goal'] = st.number_input(
            "Daily Steps Goal",
            min_value=1000,
            max_value=30000,
            value=st.session_state.goals['steps_goal']
        )

# Create DataFrame for prediction
df = pd.DataFrame({
    "Age": [age],
    "BMI": [bmi],
    "Duration": [duration],
    "Heart_Rate": [heart_rate],
    "Body_Temp": [body_temp],
    "Gender_male": [gender_encoded]
})

# Load and Process Data
try:
    calories = pd.read_csv("calories.csv")
    exercise = pd.read_csv("exercise.csv")
    dataset = exercise.merge(calories, on="User_ID").drop(columns="User_ID")
    dataset["BMI"] = round(dataset["Weight"] / ((dataset["Height"] / 100) ** 2), 2)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Prepare Train/Test Data
train_data, test_data = train_test_split(dataset, test_size=0.2, random_state=1)
train_data = train_data[["Gender", "Age", "BMI", "Duration", "Heart_Rate", "Body_Temp", "Calories"]]
test_data = test_data[["Gender", "Age", "BMI", "Duration", "Heart_Rate", "Body_Temp", "Calories"]]
train_data = pd.get_dummies(train_data, drop_first=True)
test_data = pd.get_dummies(test_data, drop_first=True)

X_train, y_train = train_data.drop("Calories", axis=1), train_data["Calories"]
X_test, y_test = test_data.drop("Calories", axis=1), test_data["Calories"]

# Train Model
model = RandomForestRegressor(n_estimators=1000, max_features=3, max_depth=6)
model.fit(X_train, y_train)

# Make Prediction
df = df.reindex(columns=X_train.columns, fill_value=0)
prediction = model.predict(df)

# Main Content
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Progress Tracking", "Trackers", "Recommendations"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Calories Burned Prediction")
        calories_metric = st.metric(
            "Predicted Calories",
            f"{round(prediction[0], 2)} kcal",
            delta=f"+{round(prediction[0]/10, 2)}%"
        )
        
        # Display factors
        st.write("Key factors affecting your calorie burn:")
        factors = {
            "Duration": f"{duration} min ({'high' if duration > 20 else 'moderate' if duration > 10 else 'low'} impact)",
            "Heart Rate": f"{heart_rate} bpm ({'high' if heart_rate > 120 else 'moderate' if heart_rate > 90 else 'low'} intensity)",
            "Body Temperature": f"{body_temp}°C ({'elevated' if body_temp > 38.5 else 'normal'})"
        }
        
        for factor, value in factors.items():
            st.write(f"• **{factor}**: {value}")
        
    with col2:
        # Workout Form
        st.subheader("💪 Log Your Workout")
        workout_date = st.date_input("Workout Date", datetime.now())
        workout_type = st.selectbox("Workout Type", [
            "Walking", "Running", "Cycling", "Swimming", 
            "Weight Training", "Yoga", "HIIT", "Other"
        ])
        additional_notes = st.text_area("Notes (optional)", max_chars=200)
        
        if st.button("Save Workout", type="primary"):
            workout = {
                'id': str(uuid.uuid4()),
                'date': workout_date.strftime("%Y-%m-%d"),
                'type': workout_type,
                'calories': round(prediction[0], 2),
                'duration': duration,
                'heart_rate': heart_rate,
                'notes': additional_notes
            }
            st.session_state.workout_history.append(workout)
            
            # Update user stats
            st.session_state.user_stats['total_workouts'] += 1
            st.session_state.user_stats['total_calories'] += workout['calories']
            st.session_state.user_stats['total_duration'] += workout['duration']
            
            # Check and update achievements
            achievements_earned = []
            
            # First workout achievement
            if not st.session_state.achievements['first_workout']['earned']:
                st.session_state.achievements['first_workout']['earned'] = True
                achievements_earned.append(st.session_state.achievements['first_workout'])
            
            # Three workouts achievement
            if st.session_state.user_stats['total_workouts'] >= 3 and not st.session_state.achievements['three_workouts']['earned']:
                st.session_state.achievements['three_workouts']['earned'] = True
                achievements_earned.append(st.session_state.achievements['three_workouts'])
            
            # Calorie milestone achievement
            if st.session_state.user_stats['total_calories'] >= 500 and not st.session_state.achievements['calorie_milestone']['earned']:
                st.session_state.achievements['calorie_milestone']['earned'] = True
                achievements_earned.append(st.session_state.achievements['calorie_milestone'])
            
            # Different workouts achievement
            unique_workouts = len(set([w['type'] for w in st.session_state.workout_history]))
            if unique_workouts >= 3 and not st.session_state.achievements['different_workouts']['earned']:
                st.session_state.achievements['different_workouts']['earned'] = True
                achievements_earned.append(st.session_state.achievements['different_workouts'])
            
            # Streak achievement logic
            today = datetime.strptime(workout_date.strftime("%Y-%m-%d"), "%Y-%m-%d")
            if st.session_state.user_stats['last_workout_date']:
                last_date = datetime.strptime(st.session_state.user_stats['last_workout_date'], "%Y-%m-%d")
                date_diff = (today - last_date).days
                
                if date_diff == 1:  # Consecutive day
                    st.session_state.user_stats['streak'] += 1
                elif date_diff == 0:  # Same day, don't increment streak
                    pass
                else:  # Streak broken
                    st.session_state.user_stats['streak'] = 1
            else:
                st.session_state.user_stats['streak'] = 1
                
            st.session_state.user_stats['last_workout_date'] = workout_date.strftime("%Y-%m-%d")
                
            # Consistency achievement
            if st.session_state.user_stats['streak'] >= 3 and not st.session_state.achievements['consistency']['earned']:
                st.session_state.achievements['consistency']['earned'] = True
                achievements_earned.append(st.session_state.achievements['consistency'])
            
            # Check and update challenges
            for i, challenge in enumerate(st.session_state.challenges):
                if not challenge['completed']:
                    if challenge['id'] == 1 and st.session_state.user_stats['streak'] >= 7:
                        st.session_state.challenges[i]['completed'] = True
                        st.info(f"🎉 Challenge completed: {challenge['name']}! You earned: {challenge['reward']}")
                    elif challenge['id'] == 2:
                        cardio_workouts = sum(1 for w in st.session_state.workout_history 
                                             if w['type'] in ['Running', 'Walking', 'Cycling', 'Swimming', 'HIIT'])
                        if cardio_workouts >= 5:
                            st.session_state.challenges[i]['completed'] = True
                            st.info(f"🎉 Challenge completed: {challenge['name']}! You earned: {challenge['reward']}")
                    elif challenge['id'] == 3 and st.session_state.user_stats['total_calories'] >= 1000:
                        st.session_state.challenges[i]['completed'] = True
                        st.info(f"🎉 Challenge completed: {challenge['name']}! You earned: {challenge['reward']}")
            
            # Show achievements earned
            st.success("Workout saved successfully!")
            st.balloons()
            
            if achievements_earned:
                st.markdown("### 🏆 Achievements Earned!")
                for achievement in achievements_earned:
                    st.markdown(f"<div class='badge'>{achievement['icon']} {achievement['name']}: {achievement['description']}</div>", unsafe_allow_html=True)
                st.markdown("---")

    # User Stats Dashboard
    st.subheader("📊 Your Fitness Stats")
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_workouts = st.session_state.user_stats['total_workouts']
        st.markdown(
            f"""
            <div class="workout-card" style="text-align: center;">
                <div style="font-size: 36px; color: #FF4B4B;">🏋️</div>
                <div style="font-size: 24px; font-weight: bold;">{total_workouts}</div>
                <div style="font-size: 14px; color: #6c757d;">Total Workouts</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        total_calories = st.session_state.user_stats['total_calories']
        st.markdown(
            f"""
            <div class="workout-card" style="text-align: center;">
                <div style="font-size: 36px; color: #FF4B4B;">🔥</div>
                <div style="font-size: 24px; font-weight: bold;">{total_calories:.0f}</div>
                <div style="font-size: 14px; color: #6c757d;">Calories Burned</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        total_duration = st.session_state.user_stats['total_duration']
        st.markdown(
            f"""
            <div class="workout-card" style="text-align: center;">
                <div style="font-size: 36px; color: #FF4B4B;">⏱️</div>
                <div style="font-size: 24px; font-weight: bold;">{total_duration:.0f}</div>
                <div style="font-size: 14px; color: #6c757d;">Minutes Exercised</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        streak = st.session_state.user_stats['streak']
        st.markdown(
            f"""
            <div class="workout-card" style="text-align: center;">
                <div style="font-size: 36px; color: #FF4B4B;">🔄</div>
                <div style="font-size: 24px; font-weight: bold;">{streak}</div>
                <div style="font-size: 14px; color: #6c757d;">Day Streak</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Recent Workouts
    if st.session_state.workout_history:
        st.subheader("💪 Recent Workouts")
        recent_history = sorted(st.session_state.workout_history, 
                              key=lambda x: x['date'], 
                              reverse=True)[:5]
        
        for i, workout in enumerate(recent_history):
            # Create a nicer workout card
            st.markdown(
                f"""
                <div class="workout-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-weight: bold; color: #6A11CB;">{workout['date']}</span> • 
                            <span style="font-weight: bold;">{workout['type']}</span>
                        </div>
                        <div>
                            <span style="margin-right: 15px;">⏱️ {workout['duration']} min</span>
                            <span>🔥 {workout['calories']} kcal</span>
                        </div>
                    </div>
                    {f'<div style="margin-top: 5px; font-style: italic; color: #6c757d;">{workout["notes"]}</div>' if workout.get('notes') else ''}
                </div>
                """,
                unsafe_allow_html=True
            )

with tab2:
    st.subheader("📈 Progress Tracking")
    
    if st.session_state.workout_history:
        history_df = pd.DataFrame(st.session_state.workout_history)
        
        # Time frame selection
        time_frame = st.radio(
            "Select Time Frame",
            ["Last 7 days", "Last 30 days", "All time"],
            horizontal=True
        )
        
        # Filter data based on time frame
        end_date = datetime.now()
        if time_frame == "Last 7 days":
            start_date = end_date - timedelta(days=7)
        elif time_frame == "Last 30 days":
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.strptime("2000-01-01", "%Y-%m-%d")
            
        # Convert date string to datetime for filtering
        history_df['date_dt'] = pd.to_datetime(history_df['date'])
        filtered_df = history_df[(history_df['date_dt'] >= start_date) & (history_df['date_dt'] <= end_date)]
        
        if filtered_df.empty:
            st.info(f"No workout data available for the selected time frame ({time_frame}).")
        else:
            # Weekly Progress
            weekly_calories = filtered_df.groupby('date')['calories'].sum().sum()
            weekly_duration = filtered_df.groupby('date')['duration'].sum().sum()
            
            col1, col2 = st.columns(2)
            
            with col1:
                calories_progress = (weekly_calories / st.session_state.goals['weekly_calories']) * 100
                st.metric("Calories Progress", 
                         f"{round(weekly_calories, 2)}/{st.session_state.goals['weekly_calories']} kcal",
                         f"{round(calories_progress, 1)}%")
                
            with col2:
                duration_progress = (weekly_duration / st.session_state.goals['weekly_duration']) * 100
                st.metric("Duration Progress",
                         f"{round(weekly_duration, 2)}/{st.session_state.goals['weekly_duration']} min",
                         f"{round(duration_progress, 1)}%")
            
            # Progress Visualizations
            st.subheader("Calories Burned Over Time")
            
            # Group by date and calculate daily sum
            daily_calories = filtered_df.groupby('date')['calories'].sum().reset_index()
            daily_calories['date'] = pd.to_datetime(daily_calories['date'])
            daily_calories = daily_calories.sort_values('date')
            
            # Create interactive line chart
            fig = px.line(
                daily_calories, 
                x='date', 
                y='calories',
                markers=True,
                title='Daily Calories Burned'
            )
            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Calories (kcal)',
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Workout Type Distribution
            st.subheader("Workout Type Distribution")
            workout_counts = filtered_df['type'].value_counts().reset_index()
            workout_counts.columns = ['Workout Type', 'Count']
            
            fig = px.pie(
                workout_counts, 
                values='Count', 
                names='Workout Type',
                hole=0.4
            )
            fig.update_layout(
                margin=dict(t=0, b=0, l=0, r=0),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Workout Intensity Analysis
            st.subheader("Workout Intensity Analysis")
            intensity_df = filtered_df[['date', 'duration', 'heart_rate', 'calories']].copy()
            
            fig = px.scatter(
                intensity_df,
                x='duration',
                y='heart_rate',
                size='calories',
                color='calories',
                hover_name='date',
                title='Workout Intensity: Duration vs Heart Rate'
            )
            fig.update_layout(
                xaxis_title='Duration (minutes)',
                yaxis_title='Heart Rate (bpm)',
                coloraxis_colorbar=dict(title='Calories')
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No workout history available. Start logging your workouts to track progress!")
        
        # Show example chart
        st.write("Here's an example of how your progress will be tracked:")
        
        # Generate sample data
        sample_dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7, 0, -1)]
        sample_calories = [150, 180, 120, 200, 160, 190, 210]
        
        sample_df = pd.DataFrame({
            'date': sample_dates,
            'calories': sample_calories
        })
        
        fig = px.line(sample_df, x='date', y='calories', markers=True, title='Example: Daily Calories Burned')
        fig.update_layout(xaxis_title='Date', yaxis_title='Calories (kcal)')
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("📊 Health Trackers")
    
    # Create tabs for different trackers
    weight_tab, steps_tab, water_tab = st.tabs(["Weight Tracker", "Step Counter", "Water Intake"])
    
    with weight_tab:
        st.subheader("⚖️ Weight Tracker")
        
        # Weight tracking form
        col1, col2 = st.columns(2)
        
        with col1:
            weight_date = st.date_input("Date", datetime.now(), key="weight_date")
            weight_value = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.1)
        
        with col2:
            notes = st.text_area("Notes (optional)", max_chars=100, key="weight_notes")
            if st.button("Log Weight", key="log_weight"):
                weight_entry = {
                    'id': str(uuid.uuid4()),
                    'date': weight_date.strftime("%Y-%m-%d"),
                    'weight': weight_value,
                    'notes': notes
                }
                st.session_state.weight_tracker.append(weight_entry)
                st.success("Weight logged successfully!")
        
        # Display weight progress
        if st.session_state.weight_tracker:
            st.markdown("### Weight Progress")
            
            # Convert data for chart
            weight_df = pd.DataFrame(st.session_state.weight_tracker)
            weight_df['date'] = pd.to_datetime(weight_df['date'])
            weight_df = weight_df.sort_values('date')
            
            # Create line chart with smoothing
            fig = px.line(
                weight_df, 
                x='date', 
                y='weight',
                markers=True,
                title='Weight Over Time',
                labels={'weight': 'Weight (kg)', 'date': 'Date'}
            )
            fig.update_traces(line=dict(shape='spline', smoothing=0.3))
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
            
            # Weight statistics
            if len(weight_df) > 1:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    initial_weight = weight_df.iloc[0]['weight']
                    latest_weight = weight_df.iloc[-1]['weight']
                    st.metric(
                        "Weight Change", 
                        f"{round(latest_weight, 1)} kg", 
                        f"{round(latest_weight - initial_weight, 1)} kg"
                    )
                
                with col2:
                    avg_weight = weight_df['weight'].mean()
                    st.metric("Average Weight", f"{round(avg_weight, 1)} kg")
                
                with col3:
                    if len(weight_df) >= 7:
                        recent_weight = weight_df.iloc[-7:]['weight'].mean()
                        st.metric("7-Day Average", f"{round(recent_weight, 1)} kg")
                    else:
                        st.metric("Recent Average", f"{round(avg_weight, 1)} kg")
        else:
            st.info("No weight data available. Start logging your weight to track progress!")
            
            # Example chart
            dates = [(datetime.now() - timedelta(days=i*5)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
            weights = [72.5, 72.2, 71.8, 71.5, 71.3, 71.0, 70.5]
            example_df = pd.DataFrame({'date': dates, 'weight': weights})
            example_df['date'] = pd.to_datetime(example_df['date'])
            
            fig = px.line(
                example_df, 
                x='date', 
                y='weight', 
                markers=True,
                title='Example: Weight Progress Chart',
                labels={'weight': 'Weight (kg)', 'date': 'Date'}
            )
            fig.update_traces(line=dict(shape='spline', smoothing=0.3))
            st.plotly_chart(fig, use_container_width=True)
    
    with steps_tab:
        st.subheader("👣 Step Counter")
        
        # Step counting form
        col1, col2 = st.columns(2)
        
        with col1:
            step_date = st.date_input("Date", datetime.now(), key="step_date")
            step_count = st.number_input("Steps", min_value=0, max_value=100000, value=5000, step=100)
        
        with col2:
            distance = round(step_count * 0.0008, 2)  # Approximate conversion from steps to km
            st.metric("Estimated Distance", f"{distance} km")
            
            if st.button("Log Steps", key="log_steps"):
                step_entry = {
                    'id': str(uuid.uuid4()),
                    'date': step_date.strftime("%Y-%m-%d"),
                    'steps': step_count,
                    'distance': distance
                }
                st.session_state.step_tracker.append(step_entry)
                st.success("Steps logged successfully!")
        
        # Display step progress
        if st.session_state.step_tracker:
            st.markdown("### Step Progress")
            
            # Calculate progress toward daily goal
            steps_goal = st.session_state.goals['steps_goal']
            latest_steps = step_count  # Default to input value
            
            # Find today's steps if they exist
            today = datetime.now().strftime("%Y-%m-%d")
            today_entries = [entry for entry in st.session_state.step_tracker if entry['date'] == today]
            if today_entries:
                latest_steps = today_entries[-1]['steps']
            
            # Progress bar
            steps_progress = (latest_steps / steps_goal) * 100
            st.markdown(f"**Today's Progress:** {latest_steps:,} / {steps_goal:,} steps ({round(steps_progress, 1)}%)")
            st.markdown(
                f"""
                <div class="progress-container">
                    <div class="progress-bar" style="width:{min(100, steps_progress)}%">
                        {round(steps_progress)}%
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Display chart of steps over time
            step_df = pd.DataFrame(st.session_state.step_tracker)
            step_df['date'] = pd.to_datetime(step_df['date'])
            step_df = step_df.sort_values('date')
            
            # Group by date and sum steps (in case of multiple entries per day)
            daily_steps = step_df.groupby('date')['steps'].sum().reset_index()
            
            fig = px.bar(
                daily_steps,
                x='date',
                y='steps',
                title='Daily Steps',
                labels={'steps': 'Steps', 'date': 'Date'}
            )
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
            
            # Step statistics
            if len(daily_steps) > 1:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    avg_steps = daily_steps['steps'].mean()
                    st.metric("Average Steps", f"{int(avg_steps):,}")
                
                with col2:
                    max_steps = daily_steps['steps'].max()
                    st.metric("Best Day", f"{int(max_steps):,} steps")
                
                with col3:
                    total_steps = daily_steps['steps'].sum()
                    st.metric("Total Steps", f"{int(total_steps):,}")
        else:
            st.info("No step data available. Start logging your steps to track progress!")
            
            # Sample progress bar
            sample_progress = 65
            st.markdown(f"**Example Progress:** 6,500 / 10,000 steps ({sample_progress}%)")
            st.markdown(
                f"""
                <div class="progress-container">
                    <div class="progress-bar" style="width:{sample_progress}%">
                        {sample_progress}%
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
    
    with water_tab:
        st.subheader("💧 Water Intake Tracker")
        
        # Initialize water tracker if not exists
        if 'water_tracker' not in st.session_state:
            st.session_state.water_tracker = []
        
        # Water tracking form
        col1, col2 = st.columns(2)
        
        with col1:
            water_date = st.date_input("Date", datetime.now(), key="water_date")
            water_amount = st.number_input("Water (ml)", min_value=0, max_value=5000, value=250, step=50)
            water_options = st.multiselect(
                "Water Type", 
                ["Water", "Coffee", "Tea", "Juice", "Sports Drink"],
                default=["Water"]
            )
        
        with col2:
            # Daily recommendation (simplified)
            recommended = 2500
            
            # Calculate today's intake
            today = datetime.now().strftime("%Y-%m-%d")
            today_entries = [entry['amount'] for entry in st.session_state.water_tracker if entry['date'] == today]
            today_total = sum(today_entries) if today_entries else 0
            
            # Display current hydration
            st.metric(
                "Today's Hydration", 
                f"{today_total} ml", 
                f"{round((today_total/recommended)*100, 1)}% of daily goal"
            )
            
            if st.button("Log Water", key="log_water"):
                water_entry = {
                    'id': str(uuid.uuid4()),
                    'date': water_date.strftime("%Y-%m-%d"),
                    'amount': water_amount,
                    'type': ', '.join(water_options)
                }
                st.session_state.water_tracker.append(water_entry)
                st.success(f"{water_amount} ml logged successfully!")
                
                # Update today's total for display
                if water_date.strftime("%Y-%m-%d") == today:
                    today_total += water_amount
        
        # Visual representation of water intake
        st.markdown("### Hydration Progress")
        water_progress = min(100, (today_total / recommended) * 100)
        
        # Display progress with a water-themed progress bar
        st.markdown(
            f"""
            <div class="progress-container">
                <div class="progress-bar" style="width:{water_progress}%; background: linear-gradient(90deg, #4F8BFF, #36D1DC);">
                    {round(water_progress)}%
                </div>
            </div>
            <p style="text-align: center; margin-top: 5px;">{today_total} ml of {recommended} ml daily goal</p>
            """, 
            unsafe_allow_html=True
        )
        
        # Water intake over time chart
        if st.session_state.water_tracker:
            # Prepare data
            water_df = pd.DataFrame(st.session_state.water_tracker)
            water_df['date'] = pd.to_datetime(water_df['date'])
            
            # Group by date and sum amounts
            daily_water = water_df.groupby('date')['amount'].sum().reset_index()
            
            # Create chart
            fig = px.line(
                daily_water,
                x='date',
                y='amount',
                markers=True,
                title='Daily Water Intake',
                labels={'amount': 'Water (ml)', 'date': 'Date'}
            )
            fig.add_hline(
                y=recommended, 
                line_dash="dash", 
                line_color="green",
                annotation_text="Daily goal"
            )
            fig.update_layout(hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No water intake data available. Start logging your hydration to track progress!")

with tab4:
    st.subheader("💪 Workout Recommendations")
    
    # Determine fitness level based on model prediction if not manually selected
    if 'fitness_level' not in locals():
        if prediction[0] > 300:
            fitness_level = "Advanced"
        elif prediction[0] > 200:
            fitness_level = "Intermediate"
        else:
            fitness_level = "Beginner"
    
    st.write(f"Based on your profile - **{fitness_level}** level:")
    
    # Create expandable sections for each recommendation
    for i, workout in enumerate(st.session_state.recommendations[fitness_level]):
        with st.expander(f"Recommendation {i+1}: {workout}"):
            # Basic details about the workout
            workout_name = workout.split(" (")[0]
            duration_str = workout.split("(")[1].split(")")[0] if "(" in workout else "varies"
            
            # Show workout details
            st.write(f"**Workout:** {workout_name}")
            st.write(f"**Recommended Duration:** {duration_str}")
            
            # Benefits section
            st.write("**Benefits:**")
            
            if "Walking" in workout_name:
                st.write("• Improves cardiovascular health")
                st.write("• Low impact exercise suitable for all fitness levels")
                st.write("• Helps maintain healthy weight")
                st.write("• Can be done anywhere with minimal equipment")
            elif "Jogging" in workout_name or "Running" in workout_name:
                st.write("• Burns calories effectively")
                st.write("• Strengthens muscles and bones")
                st.write("• Improves cardiovascular fitness")
                st.write("• Enhances mental wellbeing through endorphin release")
            elif "Cycling" in workout_name:
                st.write("• Low-impact cardio workout")
                st.write("• Strengthens lower body muscles")
                st.write("• Improves joint mobility")
                st.write("• Environmentally friendly transportation")
            elif "Swimming" in workout_name:
                st.write("• Full body workout")
                st.write("• Zero impact on joints")
                st.write("• Improves lung capacity and breathing")
                st.write("• Effective for building endurance")
            elif "HIIT" in workout_name:
                st.write("• Maximum calorie burn in minimal time")
                st.write("• Continues burning calories post-workout")
                st.write("• Improves metabolic rate")
                st.write("• No equipment necessary")
            elif "Weight" in workout_name:
                st.write("• Builds muscle mass")
                st.write("• Increases resting metabolic rate")
                st.write("• Improves functional strength")
                st.write("• Enhances bone density")
            elif "Yoga" in workout_name or "stretching" in workout_name:
                st.write("• Improves flexibility and balance")
                st.write("• Reduces stress and promotes relaxation")
                st.write("• Enhances mind-body connection")
                st.write("• Helps prevent injuries")
            elif "Circuit" in workout_name:
                st.write("• Combines strength and cardio benefits")
                st.write("• Keeps workouts interesting and varied")
                st.write("• Efficient full-body training")
                st.write("• Adaptable to different fitness levels")
            else:
                st.write("• Provides variety to your fitness routine")
                st.write("• Helps prevent plateaus in fitness progress")
                st.write("• Can target specific muscle groups")
                st.write("• Keeps workouts engaging and challenging")
                
            # Tips section
            st.write("**Tips:**")
            st.write("• Start with proper warm-up")
            st.write("• Focus on proper form and technique")
            st.write("• Stay hydrated before, during, and after workout")
            st.write("• Listen to your body and adjust intensity as needed")
            
    # Custom workout generator
    st.subheader("🏋️ Custom Workout Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_area = st.selectbox(
            "Target Area",
            ["Full Body", "Upper Body", "Lower Body", "Core", "Cardio"]
        )
        available_equipment = st.multiselect(
            "Available Equipment",
            ["None/Bodyweight", "Dumbbells", "Resistance Bands", "Kettlebells", "Yoga Mat"],
            default=["None/Bodyweight"]
        )
    
    with col2:
        workout_duration = st.slider(
            "Workout Duration (minutes)",
            min_value=10,
            max_value=60,
            value=30,
            step=5
        )
        intensity_preference = st.select_slider(
            "Intensity Level",
            options=["Light", "Moderate", "Challenging", "Intense"]
        )
    
    if st.button("Generate Custom Workout"):
        # Simple workout generator logic
        exercises = []
        
        # Base exercises by target area and equipment
        if "Full Body" in target_area:
            if "None/Bodyweight" in available_equipment:
                exercises.extend(["Jumping Jacks", "Push-ups", "Squats", "Plank", "Mountain Climbers"])
            if "Dumbbells" in available_equipment:
                exercises.extend(["Dumbbell Squat to Press", "Renegade Rows", "Dumbbell Lunges"])
            if "Kettlebells" in available_equipment:
                exercises.extend(["Kettlebell Swings", "Turkish Get-ups"])
                
        elif "Upper Body" in target_area:
            if "None/Bodyweight" in available_equipment:
                exercises.extend(["Push-ups", "Dips", "Pike Push-ups", "Pull-ups", "Inverted Rows"])
            if "Dumbbells" in available_equipment:
                exercises.extend(["Dumbbell Rows", "Overhead Press", "Bicep Curls", "Tricep Extensions"])
                
        elif "Lower Body" in target_area:
            if "None/Bodyweight" in available_equipment:
                exercises.extend(["Squats", "Lunges", "Glute Bridges", "Calf Raises", "Step-ups"])
            if "Dumbbells" in available_equipment:
                exercises.extend(["Goblet Squats", "Dumbbell Deadlifts", "Weighted Lunges"])
                
        elif "Core" in target_area:
            exercises.extend(["Plank", "Bicycle Crunches", "Russian Twists", "Mountain Climbers", "Leg Raises"])
            if "Yoga Mat" in available_equipment:
                exercises.extend(["Dead Bug", "Hollow Hold", "Superman"])
                
        elif "Cardio" in target_area:
            exercises.extend(["Jumping Jacks", "High Knees", "Burpees", "Mountain Climbers", "Jump Squats"])
            if "Kettlebells" in available_equipment:
                exercises.extend(["Kettlebell Swings"])
        
        # Adjust number of exercises and rounds based on duration
        num_exercises = min(5, len(exercises))
        selected_exercises = exercises[:num_exercises]
        
        # Adjust work/rest times based on intensity
        if intensity_preference == "Light":
            work_time = 30
            rest_time = 30
        elif intensity_preference == "Moderate":
            work_time = 40
            rest_time = 20
        elif intensity_preference == "Challenging":
            work_time = 45
            rest_time = 15
        else:  # Intense
            work_time = 50
            rest_time = 10
            
        rounds = max(2, min(5, workout_duration // (num_exercises * (work_time + rest_time) // 60)))
        
        # Display the workout
        st.markdown(f"### Your Custom {target_area} Workout")
        st.markdown(f"**Duration:** ~{workout_duration} minutes")
        st.markdown(f"**Intensity:** {intensity_preference}")
        st.markdown(f"**Format:** {rounds} rounds of {len(selected_exercises)} exercises")
        st.markdown(f"**Work/Rest Ratio:** {work_time}s work / {rest_time}s rest")
        
        st.markdown("### Exercises:")
        for i, exercise in enumerate(selected_exercises, 1):
            st.markdown(f"**{i}. {exercise}** - {work_time}s work / {rest_time}s rest")
            
        st.markdown("### Instructions:")
        st.markdown("1. Warm up for 5 minutes before starting")
        st.markdown("2. Complete all exercises in sequence")
        st.markdown(f"3. Rest for 1-2 minutes between rounds")
        st.markdown("4. Cool down and stretch for 5 minutes after completing all rounds")
        st.markdown("5. Adjust intensity as needed for your fitness level")

# Generate Report
if st.sidebar.button("Generate Fitness Report", type="primary"):
    if not st.session_state.workout_history:
        st.sidebar.warning("No workout history to generate report. Please log at least one workout.")
    else:
        # Calculate stats for report
        history_df = pd.DataFrame(st.session_state.workout_history)
        total_workouts = len(history_df)
        total_calories = history_df['calories'].sum()
        total_duration = history_df['duration'].sum()
        avg_calories = history_df['calories'].mean()
        avg_duration = history_df['duration'].mean()
        
        # Get most frequent workout type
        if 'type' in history_df.columns:
            most_frequent_type = history_df['type'].value_counts().idxmax()
        else:
            most_frequent_type = "Not available"
        
        report = f"""
        FITNESS TRACKER REPORT - {datetime.now().strftime("%Y-%m-%d")}
        
        USER PROFILE:
        - Age: {age}
        - BMI: {bmi}
        - Gender: {gender}
        - Fitness Level: {fitness_level}
        
        WORKOUT SUMMARY:
        - Total Workouts: {total_workouts}
        - Total Calories Burned: {total_calories:.2f} kcal
        - Total Duration: {total_duration:.2f} minutes
        - Average Calories per Workout: {avg_calories:.2f} kcal
        - Average Duration per Workout: {avg_duration:.2f} minutes
        - Favorite Workout Type: {most_frequent_type}
        
        PROGRESS TOWARDS GOALS:
        - Weekly Calories: {weekly_calories:.2f}/{st.session_state.goals['weekly_calories']} kcal ({calories_progress:.1f}%)
        - Weekly Duration: {weekly_duration:.2f}/{st.session_state.goals['weekly_duration']} minutes ({duration_progress:.1f}%)
        
        RECOMMENDED WORKOUTS ({fitness_level}):
        {chr(10).join(['- ' + w for w in st.session_state.recommendations[fitness_level]])}
        
        NEXT STEPS:
        1. Continue consistent workouts to reach your goals
        2. Consider increasing intensity as you progress
        3. Ensure proper recovery between workouts
        4. Stay hydrated and maintain proper nutrition
        
        Generated by Enhanced Fitness Tracker
        """
        
        # Encode report for download
        b64 = base64.b64encode(report.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="fitness_report_{datetime.now().strftime("%Y%m%d")}.txt">📥 Download Full Report</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
        
        # Show summary in sidebar
        st.sidebar.success("Report generated successfully!")
        st.sidebar.markdown("### Report Summary")
        st.sidebar.markdown(f"**Total Workouts:** {total_workouts}")
        st.sidebar.markdown(f"**Total Calories:** {total_calories:.2f} kcal")
        st.sidebar.markdown(f"**Fitness Level:** {fitness_level}")

# Achievements and Social Sharing Section
st.markdown("---")
st.subheader("🏆 Achievements & Challenges")

# Display achievements in an interactive grid
achievements_tab, challenges_tab, share_tab = st.tabs(["Achievements", "Challenges", "Share"])

with achievements_tab:
    # Check earned achievements
    earned_achievements = [a for a in st.session_state.achievements.values() if a['earned']]
    locked_achievements = [a for a in st.session_state.achievements.values() if not a['earned']]
    
    if earned_achievements:
        st.markdown("### Earned Badges")
        
        # Create a grid for badges
        cols = st.columns(min(3, len(earned_achievements)))
        for i, achievement in enumerate(earned_achievements):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="text-align: center; padding: 15px; background: linear-gradient(45deg, #6A11CB, #2575FC); 
                         border-radius: 10px; margin: 5px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                         transition: transform 0.3s ease;">
                        <div style="font-size: 36px;">{achievement['icon']}</div>
                        <div style="font-weight: bold; margin: 10px 0;">{achievement['name']}</div>
                        <div style="font-size: 14px;">{achievement['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    if locked_achievements:
        st.markdown("### Locked Achievements")
        
        # Create a grid for locked badges
        cols = st.columns(min(3, len(locked_achievements)))
        for i, achievement in enumerate(locked_achievements):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="text-align: center; padding: 15px; background: #f8f9fa; 
                         border-radius: 10px; margin: 5px; color: #6c757d; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                         filter: grayscale(100%); opacity: 0.7;">
                        <div style="font-size: 36px;">🔒</div>
                        <div style="font-weight: bold; margin: 10px 0;">{achievement['name']}</div>
                        <div style="font-size: 14px;">{achievement['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    if not earned_achievements and not locked_achievements:
        st.info("Complete workouts to earn achievements!")

with challenges_tab:
    active_challenges = [c for c in st.session_state.challenges if not c['completed']]
    completed_challenges = [c for c in st.session_state.challenges if c['completed']]
    
    if active_challenges:
        st.markdown("### Active Challenges")
        
        for challenge in active_challenges:
            st.markdown(
                f"""
                <div class="challenge-card">
                    <h4>{challenge['name']}</h4>
                    <p>{challenge['description']}</p>
                    <p><strong>Reward:</strong> {challenge['reward']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    if completed_challenges:
        st.markdown("### Completed Challenges")
        
        for challenge in completed_challenges:
            st.markdown(
                f"""
                <div class="challenge-card" style="background: linear-gradient(135deg, #28a745, #20c997);">
                    <h4>✅ {challenge['name']}</h4>
                    <p>{challenge['description']}</p>
                    <p><strong>Reward:</strong> {challenge['reward']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    if not active_challenges and not completed_challenges:
        st.info("No active challenges found.")

with share_tab:
    st.markdown("### Share Your Progress")
    
    # Calculate overall stats for sharing
    total_workouts = st.session_state.user_stats['total_workouts']
    total_calories = st.session_state.user_stats['total_calories']
    streak = st.session_state.user_stats['streak']
    
    share_message = f"I've completed {total_workouts} workouts and burned {total_calories:.0f} calories with my fitness tracker! 🏋️‍♀️"
    
    # Interactive share card
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #6f42c1, #fd7e14); color: white; padding: 20px; 
        border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; margin: 20px 0;">
            <h3>My Fitness Journey</h3>
            <p style="font-size: 18px;">🏋️‍♀️ Workouts: {total_workouts}</p>
            <p style="font-size: 18px;">🔥 Calories Burned: {total_calories:.0f}</p>
            <p style="font-size: 18px;">🔄 Current Streak: {streak} days</p>
            <p style="font-size: 18px;">💪 Achievements: {len([a for a in st.session_state.achievements.values() if a['earned']])}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Example platform buttons
    st.markdown("### Share on:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 Twitter/X", type="primary"):
            st.success("Twitter share link generated (example)")
            st.code(f"https://twitter.com/intent/tweet?text={share_message}")
    
    with col2:
        if st.button("📘 Facebook", type="primary"):
            st.success("Facebook share link generated (example)")
            st.code(f"https://www.facebook.com/sharer/sharer.php?u=https://fitnessapp.com&quote={share_message}")
    
    with col3:
        if st.button("📧 Email", type="primary"):
            st.success("Email share content generated (example)")
            st.code(f"Subject: My Fitness Journey Update\nBody: {share_message}")
    
    # Copy to clipboard option
    st.text_area("Or copy this text:", value=share_message, height=100)

# Footer
st.markdown("---")
st.markdown("### ✨ Stay Motivated, Stay Healthy! ✨")
st.markdown("Track your fitness journey and celebrate your progress.")
