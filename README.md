# 🏋️‍♂️ Fitness Tracker Pro

**Fitness Tracker Pro** is a personalized fitness dashboard designed to help users monitor workouts, set goals, track progress, and receive AI-based recommendations to maintain a healthy lifestyle. Built with a user-friendly interface and smart insights, it's your all-in-one fitness companion.

---

## 🌟 Features
- 🔐 **User Authentication**: Sign up and log in securely to access personalized data.
- 📊 **Dashboard Overview**: Get an at-a-glance summary of your calories burned, workouts logged, and fitness streaks.
- 📈 **Progress Tracking**: Visualize your fitness improvements over time with detailed charts.
- 🧠 **ML-Based Calorie Burn Prediction**: Uses models like SVM, Logistic Regression, and Random Forest to estimate calorie burn.
- 🏆 **Achievements & Challenges**: Stay motivated with unlockable fitness milestones.
- 💪 **Workout Recommendations**: AI-generated suggestions based on your profile and fitness level.
- 🧰 **Custom Workout Generator**: Build personalized routines with adjustable duration and intensity.
- 📉 **Weight Tracker**: Log your weight and view trends over time.
- 🚶 **Step & Water Intake Tracker** *(optional tab placeholders)*

---

## 🛠️ Tech Stack
| Category        | Technologies                  |
|-----------------|-------------------------------|
| Frontend        | Streamlit, HTML/CSS           |
| Backend         | Python, Streamlit Auth        |
| Machine Learning| Scikit-learn, NumPy           |
| Data Visualization | Pandas, Matplotlib, Plotly |
| Data Analysis   | Seaborn                       |

---

## 📸 UI Preview
<p align="center">
  <img src="" alt="Login Page" width="600"/>
  <p align="center"><strong>🔐 Login Page</strong></p>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Manu040405/Fitness-tracking-App/main/screenshots/register.png" alt="Register and Profile Setup" width="600"/>
  <p align="center"><strong>📝 Register and Profile Setup</strong></p>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Manu040405/Fitness-tracking-App/main/screenshots/dashboard.png" alt="Dashboard + Calorie Burn Prediction" width="600"/>
  <p align="center"><strong>📊 Dashboard + Calorie Burn Prediction</strong></p>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Manu040405/Fitness-tracking-App/main/screenshots/progress.png" alt="Progress Tracker" width="600"/>
  <p align="center"><strong>📈 Progress Tracker</strong></p>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Manu040405/Fitness-tracking-App/main/screenshots/weight.png" alt="Weight Tracker" width="600"/>
  <p align="center"><strong>⚖️ Weight Tracker</strong></p>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Manu040405/Fitness-tracking-App/main/screenshots/recommendations.png" alt="AI Workout Recommendations" width="600"/>
  <p align="center"><strong>🏋️‍♀️ AI Workout Recommendations</strong></p>
</p>

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Manu040405/Fitness-tracking-App.git
   cd Fitness-tracking-App
   ```

2. **Create Virtual Environment** (Optional but Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## 📁 Project Structure
```
Fitness-tracking-App/
│
├── app.py                      # Main Streamlit application
├── fitness_tracker.ipynb       # Model training and ML logic
├── calories.csv                # Calorie dataset
├── exercise.csv                # Exercise dataset
├── requirements.txt            # Python dependencies
├── screenshots/                # Application screenshots
└── README.md                   # Project documentation
```

---

## 🚀 Deployment Options
1. **Streamlit Cloud**
   - Connect your GitHub repository
   - Deploy directly from the `main` branch

2. **Render**
   ```bash
   # Create a web service on Render
   # Use the following build command
   pip install -r requirements.txt
   
   # Start command
   streamlit run app.py
   ```
---

## 🧠 Machine Learning Details
- **Algorithms Used**: 
  - Support Vector Machines (SVM)
  - Logistic Regression
  - Random Forest
- **Feature Engineering**: Custom preprocessing techniques
- **Model Evaluation**: Cross-validation, accuracy, and precision metrics

---

## 🙌 Acknowledgements
Special thanks to Dr. Saomya Chaudhury for mentorship, and to all peers and contributors who provided feedback and support throughout development.

---

## 📬 Contact & Connect
- **Manogna Perka**
- 📧 [manogna.perka2005@gmail.com]
- 🔗 [GitHub Profile](https://github.com/Manu040405)

---

