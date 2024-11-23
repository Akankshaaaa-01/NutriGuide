import streamlit as st
import calendar
from datetime import datetime

# Initialize session state to store meal data if not already present
if 'meal_data' not in st.session_state:
    st.session_state.meal_data = {}

# Function to generate a list of dates for the selected month and year
def generate_dates(year, month):
    num_days = calendar.monthrange(year, month)[1]  # Get the number of days in the month
    return num_days

# Function to handle meal input for a selected day
def get_meal_input(date, meal_type):
    meal = st.text_input(f"Enter {meal_type} details for {date}:", key=f"{meal_type}_{date}")
    return meal

# Function to delete a meal type for a selected day
def delete_meal(date, meal_type):
    if date in st.session_state.meal_data and meal_type in st.session_state.meal_data[date]:
        del st.session_state.meal_data[date][meal_type]
        st.success(f"{meal_type} meal for {date} has been deleted.")
    else:
        st.error(f"No {meal_type} meal found for {date}.")

# Function to display the calendar for the month
def show_calendar(year, month):
    # Get the number of days in the month
    num_days = generate_dates(year, month)
    cal = calendar.monthcalendar(year, month)
    
    st.write(f"**Calendar for {calendar.month_name[month]} {year}**")
    # Display the calendar
    html_code = '<table style="width: 100%; text-align: center;">'
    html_code += '<tr>'  # Table header with days of the week
    for day_name in calendar.day_name:
        html_code += f'<th>{day_name}</th>'
    html_code += '</tr>'
    
    for week in cal:
        html_code += '<tr>'
        for day in week:
            if day == 0:
                html_code += '<td></td>'  # Empty cell for days outside the current month
            else:
                day_str = f"{month}/{day}/{year}"
                # Check if the day has a meal plan added, and highlight it
                if day_str in st.session_state.meal_data:
                    html_code += f'<td style="background-color: lightgreen;">{day}</td>'
                else:
                    html_code += f'<td>{day}</td>'
        html_code += '</tr>'
    
    html_code += '</table>'
    st.markdown(html_code, unsafe_allow_html=True)

# Display the meal planner interface
st.title("Meal Planner Calendar")

# Select year and month for the meal planner (year from 2024 to 2028)
year = st.selectbox('Select Year', list(range(2024, 2029)), index=0)
month = st.selectbox('Select Month', list(range(1, 13)), index=0)



# Generate the list of available dates for the selected month
dates = [f"{month}/{day}/{year}" for day in range(1, generate_dates(year, month) + 1)]

# Dropdown to select a specific date
selected_date = st.selectbox('Select Date to Add/Review Meal Plan', dates)


# Display the calendar for the selected month
show_calendar(year, month) 



# Display meal input options for the selected date
if selected_date:
    # Display existing meal plans if they exist
    existing_meals = st.session_state.meal_data.get(selected_date, {})
    st.subheader(f"Meal Plan for {selected_date}")
    
    # Display existing meal plans
    meal_types = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']
    for meal_type in meal_types:
        if meal_type in existing_meals:
            st.write(f"{meal_type}: {existing_meals[meal_type]}")
        else:
            st.write(f"{meal_type}: No meal added yet")
    
    # Display meal input form horizontally
    st.subheader(f"Add or Edit Meal Plan for {selected_date}")
    col1, col2, col3, col4 = st.columns(4)
    
    # Meal input for each type (Breakfast, Lunch, Snacks, Dinner)
    with col1:
        breakfast = get_meal_input(selected_date, 'Breakfast')
    with col2:
        lunch = get_meal_input(selected_date, 'Lunch')
    with col3:
        snacks = get_meal_input(selected_date, 'Snacks')
    with col4:
        dinner = get_meal_input(selected_date, 'Dinner')
    
    # Button to save the meal plan
    if st.button('Save Meal Plan', key=f"save_button_{selected_date}"):
        st.session_state.meal_data[selected_date] = {
            'Breakfast': breakfast if breakfast else existing_meals.get('Breakfast', ''),
            'Lunch': lunch if lunch else existing_meals.get('Lunch', ''),
            'Snacks': snacks if snacks else existing_meals.get('Snacks', ''),
            'Dinner': dinner if dinner else existing_meals.get('Dinner', '')
        }
        st.success(f"Meal Plan for {selected_date} has been saved.")
    
    # Button to delete meal plan for the selected date
    if st.button(f"Delete Meal Plan for {selected_date}", key=f"delete_button_{selected_date}"):
        if selected_date in st.session_state.meal_data:
            del st.session_state.meal_data[selected_date]
            st.success(f"Meal Plan for {selected_date} has been deleted.")
        else:
            st.error(f"No meal plan found for {selected_date}.")
