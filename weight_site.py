import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Weight & Calorie Advisor",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Dark Mode CSS Only ---
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

/* Button Styling */
.stButton>button {
    background: linear-gradient(45deg, #2196F3, #1976D2) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    height: 3em !important;
    width: 100% !important;
    font-weight: bold !important;
    font-size: 1.1em !important;
    border: none !important;
    transition: all 0.3s ease !important;
}
.stButton>button:hover {
    background: linear-gradient(45deg, #1976D2, #1565C0) !important;
    color: #FFFFFF !important;
    transform: scale(1.05) !important;
}

.stProgress > div > div > div {
    background-color: #9b59b6 !important;
}

h1, h2, h3, h4, h5, h6, label {
    text-align: center;
    color: white !important;
}
.stRadio, .stSelectbox, .stNumberInput {
    color: white !important;
}
</style>
"""

# --- Apply Dark Mode ---
st.markdown(dark_mode_css, unsafe_allow_html=True)

# --- App Title ---
st.title("🏋️‍♂️ Weight & Calorie Advisor")
st.markdown("### Unlock personalized insights into your daily energy needs and health goals 💡")
st.divider()

# --- Input Form ---
with st.form("calorie_form"):
    st.markdown("#### 📝 Enter Your Details")
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("🧍 Gender", ["Male", "Female"])
        age = st.number_input("🎂 Age (years)", min_value=15, max_value=100, step=1)
        activity = st.selectbox(
            "⚡ Activity Level",
            ["Sedentary: Little to no exercise", "Lightly Active: 1-3x/week", 
             "Moderately Active: 3-5x/week", "Very Active: 6-7x/week", 
             "Extremely Active: Physical job or 2x/day training"]
        )
    
    with col2:
        height = st.number_input("📏 Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
        weight = st.number_input("⚖️ Weight (kg)", min_value=30.0, max_value=200.0, step=0.1)
        goal = st.selectbox(
            "🎯 Goal",
            ["Lose Weight 🧘‍♀️", "Maintain Weight ⚖️", "Gain Muscle 🏗️"]
        )
    
    submitted = st.form_submit_button("💥 Calculate My Calories")

# --- Calculation Logic ---
if submitted:
    if age < 15 or age > 100 or height < 100 or height > 250 or weight < 30 or weight > 200:
        st.error("❌ Please ensure all inputs are within the specified ranges.")
    else:
        # BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        # BMR
        if gender == "Male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        # Activity Multiplier
        activity_multipliers = {
            "Sedentary: Little to no exercise": 1.2,
            "Lightly Active: 1-3x/week": 1.375,
            "Moderately Active: 3-5x/week": 1.55,
            "Very Active: 6-7x/week": 1.725,
            "Extremely Active: Physical job or 2x/day training": 1.9
        }
        activity_factor = activity_multipliers[activity]
        maintenance = bmr * activity_factor
        
        # Goal Adjustment
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
        
        # Output
        st.subheader("💡 Your Personalized Results:")
        st.success(f"{emoji} **{goal_text} Calorie Target:** {target_calories:.0f} kcal/day")
        st.info(f"**Maintenance Calories:** {maintenance:.0f} kcal/day (BMR: {bmr:.0f} kcal/day)")
        st.info(f"**Your BMI:** {bmi:.1f} ({'Underweight' if bmi < 18.5 else 'Normal' if bmi < 25 else 'Overweight' if bmi < 30 else 'Obese'})")
        
        # Progress bar
        if goal == "Maintain Weight ⚖️":
            progress = 0.5
        else:
            deficit_surplus = abs(target_calories - maintenance)
            progress = min(deficit_surplus / 500, 1.0)
        st.progress(progress)
        st.caption("Progress bar indicates the intensity of your calorie adjustment relative to maintenance.")
        
        # Personalized Advice
        st.markdown("---")
        st.markdown("#### 🧠 Personalized Advice:")
        if bmi < 18.5:
            st.warning("🍔 Underweight: Focus on nutrient-dense foods and strength training.")
        elif 18.5 <= bmi < 25:
            st.success("✅ Normal range: Great job maintaining a healthy weight!")
        elif 25 <= bmi < 30:
            st.info("🏃 Overweight: Try adding cardio and monitoring portion sizes.")
        else:
            st.error("🏥 Obesity: Consult a healthcare professional for guidance.")
        
        if "Lose" in goal:
            st.markdown("- Aim for a 500 kcal deficit for ~0.5 kg/week loss.")
        elif "Gain" in goal:
            st.markdown("- Target a 300 kcal surplus for muscle gain.")
        else:
            st.markdown("- Maintain consistency to stay at your current weight.")
        
        st.caption("💬 Tip: Adjust calories by ±250 kcal if progress stalls.")
else:
    st.info("👆 Fill in your details above and click **Calculate My Calories** to get started!")

# --- Footer ---
st.divider()
st.markdown("""
    <center>
        <small>Built with ❤️ LIFT HEALTHY | Dark Mode Enabled | Formula: Harris-Benedict BMR + Activity Multipliers + Goal Adjustments</small><br>
        <small>⚠️ For informational purposes only. Consult a healthcare professional for personalized advice.</small>
    </center>
""", unsafe_allow_html=True)
