import streamlit as st
from datetime import datetime, timedelta

import google.generativeai as genai

API_KEY = "AIzaSyBLcvSecNLxix26DJDK2o5jNtNvLC4owTQ"
genai.configure(api_key=API_KEY)

import streamlit as st
from datetime import datetime, timedelta

# Initialize session state for chat history and service selection
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "service_selected" not in st.session_state:
    st.session_state["service_selected"] = False
if "selected_service" not in st.session_state:
    st.session_state["selected_service"] = None
if "selected_description" not in st.session_state:
    st.session_state["selected_description"] = None

# Define the services with numbered options and their descriptions
services = {
    "1": {"name": "Invite Friends", "description": "Users can send referrals directly via the chatbot (SMS, WhatsApp, Email), track referral rewards, and see how many friends have successfully signed up."},
    "2": {"name": "Easyload & Bill Payments", "description": "Facilitates mobile top-ups and bill payments through the chatbot interface."},
    "3": {"name": "Rewards Management", "description": "Track and redeem loyalty points, cashback, or rewards. Suggest relevant promotions and offers."},
    "4": {"name": "Utility Bill Payments", "description": "Allows users to view and pay utility bills seamlessly through the chatbot."},
    "5": {"name": "Savings and Goals", "description": "Set savings goals (e.g., vacations, purchases) and automate small regular contributions."},
    "6": {"name": "Debit Card Management", "description": "Request new or replacement debit cards, activate cards, and manage queries."},
    "7": {"name": "One-Stop Shop for All Services", "description": "Provides a directory for all available Easypaisa services and quick access links."},
    "8": {"name": "Ticket Booking", "description": "Automate ticket booking for events or travel, with real-time updates and reminders."},
    "9": {"name": "Retail Locator (Near Retailer)", "description": "Find the nearest Easypaisa agent or cash withdrawal location using geo-based search."},
    "10": {"name": "Security and Fraud Detection", "description": "Receive real-time alerts for suspicious transactions and manage card blocking or unblocking."},
    "11": {"name": "Customer Support", "description": "Assist with FAQs, troubleshooting, and escalate issues to human agents if needed."},
    "12": {"name": "Additional Features", "description": "Introduce investment options, subscription management, and related services."}
}

# Function to reset the session state for going to the main menu
def go_to_main_menu():
    st.session_state["messages"] = []
    st.session_state["service_selected"] = False
    st.session_state["selected_service"] = None
    st.session_state["selected_description"] = None
    st.rerun()  # Refresh the app to display the main menu


# Function to get response from Gemini API
def get_gemini_response(question, service_name, service_description):
    model = genai.GenerativeModel("gemini-pro")
    dynamic_prompt = f"""
    You are a chatbot specializing in Easypaisa, Pakistan's digital banking app.
    Focus exclusively on the selected service: {service_name}.
    Description: {service_description}
    User query: {question}
    Provide concise, realistic answers strictly related to this service. Include conversational flow where relevant.
    If the user's query pertains to a different service or is outside Easypaisa's offerings, politely inform them.
    """
    response = model.generate_content(dynamic_prompt)
    return response.text


# Dummy functionality for "Ticket Booking"
def handle_ticket_booking(user_input):
    if "lahore to islamabad" in user_input.lower():
        return "The fare for the ticket by road from Lahore to Islamabad is 2100 PKR per person. Please specify the number of tickets."
    elif "tickets" in user_input.lower():
        try:
            num_tickets = int([word for word in user_input.split() if word.isdigit()][0])
            total_fare = 2100 * num_tickets
            scheduled_time = datetime.now() + timedelta(hours=2)
            return f"Your total fare for {num_tickets} ticket(s) is {total_fare} PKR. The ticket is scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}. Your ticket has been booked under consumer ID: 123456789. Details have been sent to your email."
        except (IndexError, ValueError):
            return "Please specify a valid number of tickets."
    return None  # Delegate to Gemini API for other queries

# Dummy functionality for "Utility Bill Payments"
def handle_bill_payment(user_input):
    if "electricity bill" in user_input.lower():
        return "Please provide your consumer ID."
    elif "329583624" in user_input:
        due_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        return f"The bill for consumer ID 329583624 is 40,000 PKR, and the due date is {due_date}. Do you want to pay the bill?"
    elif "yes" in user_input.lower():
        return "40,000 PKR will be deducted from your account. The bill details will be sent to your email."
    elif "no" in user_input.lower():
        return "Okay, but make sure you pay the bill before the due date."
    return None  # Delegate to Gemini API for other queries

# Display welcome message and options if no service is selected
if not st.session_state["service_selected"]:
    st.header("✨Welcome to the Easypaisa Chatbot!")
    st.write("Please select a service by typing the corresponding number:")
    for number, service in services.items():
        st.write(f"{number}. {service['name']}")

    # Input for the user to select a service
    service_input = st.text_input("Enter the number of your desired service:")

    if service_input in services:
        st.session_state["service_selected"] = True
        st.session_state["selected_service"] = services[service_input]["name"]
        st.session_state["selected_description"] = services[service_input]["description"]
        st.session_state["messages"].append({
            "role": "assistant",
            "content": f"You have selected: {services[service_input]['name']}. You can now ask questions about this service."
        })
        st.rerun()  # Refresh the app to display the selected service interface
    elif service_input:
        st.write("Invalid input. Please enter a valid number from the list.")

# Display the selected service interface
if st.session_state["service_selected"]:
    selected_service = st.session_state["selected_service"]
    selected_description = st.session_state["selected_description"]

    st.header(f"Selected Service: {selected_service}")

    # Display chat history
    for message in st.session_state["messages"]:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.markdown(content)

    # Chat input box
    prompt = st.chat_input(f"Ask about {selected_service}:")

    if prompt:
        # Check if the user wants to go to the main menu
        if "i want to go to the main menu" in prompt.lower():
            go_to_main_menu()  # Reset session and return to the main menu
            st.stop()  # Prevent further execution

        # Add user message to the session state
        st.session_state["messages"].append({"role": "user", "content": prompt})

        # Handle dummy functionalities
        if selected_service == "Ticket Booking":
            response = handle_ticket_booking(prompt) or get_gemini_response(prompt, selected_service, selected_description)
        elif selected_service == "Utility Bill Payments":
            response = handle_bill_payment(prompt) or get_gemini_response(prompt, selected_service, selected_description)
        else:
            # Get response from Gemini API for other services
            response = get_gemini_response(prompt, selected_service, selected_description)

        # Add assistant message to the session state
        st.session_state["messages"].append({"role": "assistant", "content": response})

        # Display user and assistant messages
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
