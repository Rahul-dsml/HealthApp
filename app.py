import streamlit as st
from datetime import datetime

# Ensure session state has a default step and user_data dictionary
if "step" not in st.session_state:
    st.session_state["step"] = "register"
if "user_data" not in st.session_state:
    st.session_state["user_data"] = {}

# Registration and Profile Setup
def register_user():
    st.title("Personal Health Assistant - Registration")

    email = st.text_input("Email")
    name = st.text_input("Name")
    if st.button("Register"):
        if email and name:
            st.session_state["user_data"]["email"] = email
            st.session_state["user_data"]["name"] = name
            st.success("Registered successfully! Proceed to profile setup.")
            st.session_state["step"] = "profile_setup"
        else:
            st.error("Please fill in all fields.")

def profile_setup():
    st.title("Profile Setup")

    age = st.number_input("Age", min_value=0)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    dietary_pref = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])
    height = st.number_input("Height (cm)", min_value=50)
    weight = st.number_input("Weight (kg)", min_value=20)
    medical_conditions = st.text_area("Medical Conditions (e.g., diabetes, hypertension)")
    goal = st.selectbox("Your Goal", ["Weight Loss", "Muscle Gain", "Maintain Health"])

    if st.button("Save Profile"):
        st.session_state["user_data"].update({
            "age": age,
            "sex": sex,
            "dietary_pref": dietary_pref,
            "height": height,
            "weight": weight,
            "medical_conditions": medical_conditions,
            "goal": goal
        })
        st.success("Profile saved successfully!")
        st.session_state["step"] = "chatbot"

# Chatbot Interface
def chatbot_interface():
    if "name" in st.session_state["user_data"]:
        st.title(f"Welcome, {st.session_state['user_data']['name']}!")
    else:
        st.title("Welcome!")

    # Greeting
    st.write(f"Hi {st.session_state['user_data'].get('name', 'User')}, how are you feeling today?")
    
    # Meal input (Text)
    meal_description = st.text_input("Describe your meal (e.g., 'I ate 2 chapatis and dal')")

    # Meal processing simulation
    if st.button("Analyze Meal"):
        if meal_description:
            # Simulate analysis and provide feedback
            st.write(f"Analyzing: {meal_description}")
            calories = 250  # Mock calorie value
            carbs = 30  # Mock carbs value
            protein = 10  # Mock protein value
            fat = 8  # Mock fat value
            st.write("Nutritional breakdown:")
            st.write(f"Calories: {calories} kcal")
            st.write(f"Carbohydrates: {carbs} g")
            st.write(f"Protein: {protein} g")
            st.write(f"Fat: {fat} g")
            st.session_state["last_meal"] = meal_description
        else:
            st.error("Please enter a meal description.")

    # Meal Recommendation based on user goal
    if "last_meal" in st.session_state:
        goal = st.session_state["user_data"].get("goal", "Maintain Health")
        if goal == "Weight Loss":
            st.write("Recommended for next meal: A light salad with a protein source like paneer or tofu.")
        elif goal == "Muscle Gain":
            st.write("Recommended for next meal: High-protein meal with chicken or lentils.")
        else:
            st.write("Recommended for next meal: A balanced meal with protein, carbs, and vegetables.")

# Main Flow Control
if st.session_state["step"] == "register":
    register_user()
if st.session_state["step"] == "profile_setup":
    profile_setup()
if st.session_state["step"] == "chatbot":
    chatbot_interface()
