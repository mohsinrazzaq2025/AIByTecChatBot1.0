import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# ----------------------
# Load Environment Variables
# ----------------------
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
openai.api_key = os.getenv("OPENAI_API_KEY")
PDF_PATH = "./Aibytec fine tuned data.pdf"
WEBSITE_URL = "https://www.aibytec.com/"
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ----------------------
# Functions
# ----------------------

# Function to send email
def send_email(name, email, contact_no, area_of_interest):
    subject = "New User Profile Submission"
    body = f"""
    New Student Profile Submitted:

    Name: {name}
    Email: {email}
    Contact No.: {contact_no}
    Area of Interest: {area_of_interest}
    """
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = RECEIVER_EMAIL
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        server.quit()
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Function to extract PDF text
def extract_pdf_text(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        return f"Error scraping website: {e}"

# Function to generate OpenAI response
def chat_with_ai(user_question, website_text, pdf_text, chat_history):
    combined_context = f"Website Content:\n{website_text}\n\nPDF Content:\n{pdf_text}"
    messages = [{"role": "system", "content": "You are a helpful assistant. Use the provided content."}]
    for entry in chat_history:
        messages.append({"role": "user", "content": entry['user']})
        messages.append({"role": "assistant", "content": entry['bot']})
    messages.append({"role": "user", "content": f"{combined_context}\n\nQuestion: {user_question}"})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=256,
            temperature=0.7,
            stream=False
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating response: {e}"

# Function to send WhatsApp message
def send_whatsapp_message(to_number, message_body):
    try:
        message = twilio_client.messages.create(
            from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
            body=message_body,
            to=f"whatsapp:{to_number}"
        )
        print(f"Message sent with SID: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

# ----------------------
# Streamlit UI and App Logic
# ----------------------

st.set_page_config(page_title="Student Profile & AI Chatbot", layout="wide")

# Session State Initialization
if "page" not in st.session_state:
    st.session_state['page'] = 'form'
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

# ----------------------
# PAGE 1: User Info Form
# ----------------------
if st.session_state['page'] == 'form':

    with st.form(key="user_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        contact_no = st.text_input("Contact No.")
        area_of_interest = st.text_input("Area of Interest")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Proceed to Chat")
        with col2:
            continue_chat = st.form_submit_button("Skip and Join Chat")
        
        if submitted:
            if name and email and contact_no and area_of_interest:
                send_email(name, email, contact_no, area_of_interest)
                st.session_state['page'] = 'chat'
                st.rerun()
            else:
                st.warning("Please fill out all fields.")
        
        if continue_chat:
            st.session_state['page'] = 'chat'
            st.rerun()

# ----------------------
# PAGE 2: Chatbot Interface
# ----------------------
elif st.session_state['page'] == 'chat':
    for entry in st.session_state['chat_history']:
        if entry['user']:
            st.markdown(f"**You:** {entry['user']}")
        if entry['bot']:
            st.markdown(f"**Bot:** {entry['bot']}")

    pdf_text = extract_pdf_text(PDF_PATH) if os.path.exists(PDF_PATH) else "PDF file not found."
    website_text = scrape_website(WEBSITE_URL)

    user_input = st.chat_input("Type your question here...")
    if user_input:
        send_whatsapp_message("+14155238886", "Test message from chatbot")  # Change number to test
        st.session_state['chat_history'].append({"user": user_input, "bot": ""})
        bot_response = chat_with_ai(user_input, website_text, pdf_text, st.session_state['chat_history'])
        st.session_state['chat_history'][-1]['bot'] = bot_response
        send_whatsapp_message("+YourPhoneNumber", f"New visitor message: {user_input}")  # Update with your phone number
        st.rerun()

# ----------------------
# Webhook Handler (Updated to Use st.query_params)
# ----------------------
def handle_whatsapp_webhook():
    """Handles incoming WhatsApp webhook requests"""
    from flask import request

    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')
    
    # Get the content from the website and PDF
    website_text = scrape_website(WEBSITE_URL)
    pdf_text = extract_pdf_text(PDF_PATH)

    # Generate AI response
    bot_response = chat_with_ai(incoming_msg, website_text, pdf_text, st.session_state.get('chat_history', []))

    # Store chat history
    st.session_state['chat_history'].append({"user": incoming_msg, "bot": bot_response})

    # Send the response back to the user via Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(bot_response)

    return str(twilio_response)

# Add an endpoint in the Streamlit app
if 'whatsapp' in st.query_params:
    st.write(handle_whatsapp_webhook())
