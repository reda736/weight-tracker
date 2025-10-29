import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Weight & Calorie Advisor",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Mode Selection with Session State for Persistence ---
if 'mode' not in st.session_state:
    st.session_state.mode = "Clair (Light)"

mode = st.radio(
    "🌗 Choose Mode:",
    ["Clair (Light)", "Sombre (Dark)"],
    index=["Clair (Light)", "Sombre (Dark)"].index(st.session_state.mode),
    horizontal=True
)
st.session_state.mode = mode

# --- Define Enhanced CSS for Both Modes ---
light_mode_css = """
<style>
[data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
    background-color: #f0f4f8 !important;
    color: #2c3e50 !important;
}
.main {
    background-color: #ffffff !important;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.stButton>button {
    background: linear-gradient(45deg, #4CAF50, #45a049) !important;
    color: white !important;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
    font-size: 1.1em;
    border: none;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(45deg, #45a049, #3e8e41) !important;
    transform: scale(1.05);
}
.stProgress > div > div > div {
    background-color: #4CAF50 !important;
}
h1, h2, h3, h4, h5, h6, label {
    text-align: center;
    color: #2c3e50 !important;
}
.stRadio, .stRadio label, .stSelectbox, .stNumberInput {
    color: #2c3e50 !important;
}
</style>
"""

dark_mode_css = """
<style>
button,input,select {
    background: #000000 !important;
    color:white !important;
}

[data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
    background-color: #0e1117 !important;
    color: #fafafa !important;
}
.main {
    background-color: #1e1e2f !important;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}
/* BOUTON RECONSTRUIT COMPLETEMENT POUR MODE SOMBRE */
.stButton>button {
    /* Background: blue gradient */
    background: linear-gradient(45deg, #2196F3, #1976D2) !important;
    background-color: #2196F3 !important;
    background-image: linear-gradient(45deg, #2196F3, #1976D2) !important;
    
    /* Texte: white */
    color: #FFFFFF !important;
    
    /* Style du bouton */
    border-radius: 10px !important;
    height: 3em !important;
    width: 100% !important;
    font-weight: bold !important;
    font-size: 1.1em !important;
    border: none !important;
    transition: all 0.3s ease !important;
    
    /* Force la couleur sur tous les enfants */
    * {
        color: #FFFFFF !important;
    }
}

/* Hover: darker blue, texte reste white */
.stButton>button:hover {
    background: linear-gradient(45deg, #1976D2, #1565C0) !important;
    background-color: #1976D2 !important;
    color: #FFFFFF !important;
    transform: scale(1.05) !important;
}

.stButton>button:hover * {
    color: #FFFFFF !important;
}

/* Focus et Active: texte white */
.stButton>button:focus,
.stButton>button:active {
    color: #FFFFFF !important;
    background: linear-gradient(45deg, #2196F3, #1976D2) !important;
}

.stButton>button:focus *,
.stButton>button:active * {
    color: #FFFFFF !important;
}

.stProgress > div > div > div {
    background-color: #9b59b6 !important;
}
h1, h2, h3, h4, h5, h6, label {
    text-align: center;
    color: white !important;
}
.stRadio, .stRadio label, .stSelectbox, .stNumberInput {
    color: white !important;
}
</style>
"""

# --- Apply the Chosen Theme ---
st.markdown(dark_mode_css if "Sombre" in st.session_state.mode else light_mode_css, unsafe_allow_html=True)

# --- App Title ---
st.title("🏋️‍♂️ Weight & Calorie Advisor")
st.markdown("### Unlock personalized insights into your daily energy needs and health goals 💡")
st.divider()

# --- Input Form for Better User Experience ---
with st.form("calorie_form"):
    st.markdown("#### 📝 Enter Your Details")
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("🧍 Gender", ["Male", "Female"], help="Select your biological gender for accurate calculations.")
        age = st.number_input("🎂 Age (years)", min_value=15, max_value=100, step=1, help="Age must be between 15 and 100.")
        activity = st.selectbox(
            "⚡ Activity Level",
            ["Sedentary: Little to no exercise", "Lightly Active: 1-3x/week", "Moderately Active: 3-5x/week", "Very Active: 6-7x/week", "Extremely Active: Physical job or 2x/day training"],
            help="Choose the level that best describes your weekly activity."
        )
    
    with col2:
        height = st.number_input("📏 Height (cm)", min_value=100.0, max_value=250.0, step=0.1, help="Height in centimeters.")
        weight = st.number_input("⚖️ Weight (kg)", min_value=30.0, max_value=200.0, step=0.1, help="Current weight in kilograms.")
        goal = st.selectbox(
            "🎯 Goal",
            ["Lose Weight 🧘‍♀️", "Maintain Weight ⚖️", "Gain Muscle 🏗️"],
            help="Select your primary fitness goal."
        )
    
    # Submit Button
    submitted = st.form_submit_button("💥 Calculate My Calories")

# --- Calculation Logic ---
if submitted:
    # Input Validation
    if age < 15 or age > 100 or height < 100 or height > 250 or weight < 30 or weight > 200:
        st.error("❌ Please ensure all inputs are within the specified ranges.")
    else:
        # Step 1: Calculate BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        # Step 2: BMR Calculation using Harris-Benedict Equation
        if gender == "Male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        # Step 3: Activity Multiplier
        activity_multipliers = {
            "Sedentary: Little to no exercise": 1.2,
            "Lightly Active: 1-3x/week": 1.375,
            "Moderately Active: 3-5x/week": 1.55,
            "Very Active: 6-7x/week": 1.725,
            "Extremely Active: Physical job or 2x/day training": 1.9
        }
        activity_factor = activity_multipliers[activity]
        maintenance = bmr * activity_factor
        
        # Step 4: Goal Adjustment
        if "Lose" in goal:
            target_calories = maintenance - 500
            emoji = "🔥"
            goal_text = "Weight Loss"
        elif "Gain" in goal:
            target_calories = maintenance + 300
            emoji = "💪"
            goal_text = "Muscle Gain"
        else:
            target_calories = maintenance
            emoji = "⚖️"
            goal_text = "Maintenance"
        
        # Step 5: Output Results
        st.subheader("💡 Your Personalized Results:")
        st.success(f"{emoji} **{goal_text} Calorie Target:** {target_calories:.0f} kcal/day")
        st.info(f"**Maintenance Calories:** {maintenance:.0f} kcal/day (BMR: {bmr:.0f} kcal/day)")
        st.info(f"**Your BMI:** {bmi:.1f} ({'Underweight' if bmi < 18.5 else 'Normal' if bmi < 25 else 'Overweight' if bmi < 30 else 'Obese'})")
        
        # Visual Progress Bar (Relative to Maintenance)
        if goal == "Maintain Weight ⚖️":
            progress = 0.5  # Neutral for maintenance
        else:
            deficit_surplus = abs(target_calories - maintenance)
            progress = min(deficit_surplus / 500, 1.0)  # Scale to 0-1
        st.progress(progress)
        st.caption("Progress bar indicates the intensity of your calorie adjustment relative to maintenance.")
        
        # Personalized Advice Based on BMI and Goal
        st.markdown("---")
        st.markdown("#### 🧠 Personalized Advice:")
        if bmi < 18.5:
            st.warning("🍔 Your BMI indicates underweight. Focus on nutrient-dense foods and strength training to gain healthy weight.")
        elif 18.5 <= bmi < 25:
            st.success("✅ Your BMI is in the normal range. Great job maintaining a healthy weight!")
        elif 25 <= bmi < 30:
            st.info("🏃 Your BMI suggests overweight. Consider increasing cardio and monitoring portion sizes for gradual weight loss.")
        else:
            st.error("🏥 Your BMI indicates obesity. Consult a healthcare professional for personalized advice, including diet and exercise plans.")
        
        # Goal-Specific Tips
        if "Lose" in goal:
            st.markdown("- Aim for a 500 kcal deficit for ~0.5 kg/week loss. Combine with cardio and strength training.")
        elif "Gain" in goal:
            st.markdown("- Target a 300 kcal surplus for muscle gain. Prioritize protein-rich foods and progressive overload in workouts.")
        else:
            st.markdown("- Maintain balance with consistent activity and portion control to stay at your current weight.")
        
        st.caption("💬 Tip: Track your progress weekly and adjust calories by ±250 kcal if needed. Always consult a doctor before major changes.")

else:
    st.info("👆 Fill in your details above and click **Calculate My Calories** to get started!")

# --- Footer ---
st.divider()
st.markdown(f"""
    <center>
        <small>Built with ❤️ LIFT HEALTHY | Mode: <b>{st.session_state.mode}</b> | Formula: Harris-Benedict BMR + Activity Multipliers + Goal Adjustments</small><br>
        <small>⚠️ This is for informational purposes only. Consult a healthcare professional for personalized advice.</small>
    </center>
""", unsafe_allow_html=True)
