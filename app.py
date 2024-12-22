# import streamlit as st
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from PyPDF2 import PdfReader
# import requests
# from bs4 import BeautifulSoup
# import openai
# import os
# from dotenv import load_dotenv

# # ----------------------
# # Load Environment Variables
# # ----------------------
# load_dotenv()

# SENDER_EMAIL = os.getenv("SENDER_EMAIL")
# SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
# RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
# openai.api_key = os.getenv("OPENAI_API_KEY")
# PDF_PATH = "./Aibytec fine tuned data.pdf"
# WEBSITE_URL = "https://www.aibytec.com/"

# # ----------------------
# # Functions
# # ----------------------

# # Function to send email
# def send_email(name, email, contact_no, area_of_interest):
#     subject = "New User Profile Submission"
#     body = f"""
#     New Student Profile Submitted:

#     Name: {name}
#     Email: {email}
#     Contact No.: {contact_no}
#     Area of Interest: {area_of_interest}
#     """
#     message = MIMEMultipart()
#     message['From'] = SENDER_EMAIL
#     message['To'] = RECEIVER_EMAIL
#     message['Subject'] = subject
#     message.attach(MIMEText(body, 'plain'))
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
#         server.quit()
#         st.success("Email sent successfully!")
#     except Exception as e:
#         st.error(f"Error sending email: {e}")

# # Function to extract PDF text
# def extract_pdf_text(file_path):
#     try:
#         reader = PdfReader(file_path)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text() + "\n"
#         return text
#     except Exception as e:
#         st.error(f"Error reading PDF: {e}")
#         return ""

# # Function to scrape website content
# def scrape_website(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, "html.parser")
#         return soup.get_text()
#     except Exception as e:
#         return f"Error scraping website: {e}"

# # Function to generate OpenAI response
# def chat_with_ai(user_question, website_text, pdf_text, chat_history):
#     combined_context = f"Website Content:\n{website_text}\n\nPDF Content:\n{pdf_text}"
#     messages = [{"role": "system", "content": "You are a helpful assistant. Use the provided content."}]
#     for entry in chat_history:
#         messages.append({"role": "user", "content": entry['user']})
#         messages.append({"role": "assistant", "content": entry['bot']})
#     messages.append({"role": "user", "content": f"{combined_context}\n\nQuestion: {user_question}"})

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             max_tokens=256,
#             temperature=0.7,
#             stream=False
#         )
#         return response['choices'][0]['message']['content']
#     except Exception as e:
#         return f"Error generating response: {e}"

# # ----------------------
# # Streamlit UI and App Logic
# # ----------------------

# st.set_page_config(page_title="Student Profile & AI Chatbot", layout="wide")

# # Session State Initialization
# if "page" not in st.session_state:
#     st.session_state['page'] = 'form'
# if "chat_history" not in st.session_state:
#     st.session_state['chat_history'] = []

# # ----------------------
# # PAGE 1: User Info Form
# # ----------------------
# if st.session_state['page'] == 'form':

#     with st.form(key="user_form"):
#         name = st.text_input("Name")
#         email = st.text_input("Email")
#         contact_no = st.text_input("Contact No.")
#         area_of_interest = st.text_input("Area of Interest")
        
#         # Create two columns for buttons
#         col1, col2 = st.columns(2)
#         with col1:
#             submitted = st.form_submit_button("Proceed to Chat ")
#         with col2:
#             continue_chat = st.form_submit_button(" Skip and Join Chat")
        
#         if submitted:
#             if name and email and contact_no and area_of_interest:
#                 send_email(name, email, contact_no, area_of_interest)
#                 st.session_state['page'] = 'chat'
#                 st.rerun()
#             else:
#                 st.warning("Please fill out all fields.")
        
#         # If user clicks "Continue Chat with AIByTec"
#         if continue_chat:
#             st.session_state['page'] = 'chat'
#             st.rerun()

# # ----------------------
# # PAGE 2: Chatbot Interface
# # ----------------------
# elif st.session_state['page'] == 'chat':
#     # Display chat history without headings
#     for entry in st.session_state['chat_history']:
#         # User Message
#         st.markdown(
#             f"""
#             <div style="
#                 background-color: #78bae4; 
#                 padding: 10px; 
#                 border-radius: 10px; 
#                 margin-bottom: 10px;
#                 width: fit-content;
#                 max-width: 80%;
#                 overflow: hidden;
#             ">
#                 {entry['user']}
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )

#         # Assistant Message
#         st.markdown(
#             f"""
#             <div style="
#                 background-color:  #D3D3D3; 
#                 padding: 10px; 
#                 border-radius: 10px; 
#                 margin-bottom: 10px;
#                 margin-left: auto;
#                 width: fit-content;
#                 max-width: 80%;
#                 overflow: hidden;
#             ">
#                 {entry['bot']}
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )

#     # Load PDF and Website content once
#     pdf_text = extract_pdf_text(PDF_PATH) if os.path.exists(PDF_PATH) else "PDF file not found."
#     website_text = scrape_website(WEBSITE_URL)

#     # Fixed input bar at bottom
#     user_input = st.chat_input("Type your question here...", key="user_input_fixed")

#     if user_input:
#         # Display bot's response
#         with st.spinner("Generating response..."):
#             bot_response = chat_with_ai(user_input, website_text, pdf_text, st.session_state['chat_history'])
        
#         # Append user query and bot response to chat history
#         st.session_state['chat_history'].append({"user": user_input, "bot": bot_response})
        
#         # Re-run to display updated chat history
#         st.rerun()












# import streamlit as st
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from PyPDF2 import PdfReader
# import requests
# from bs4 import BeautifulSoup
# import openai
# import os
# from dotenv import load_dotenv
# from flask import Flask, request
# from twilio.rest import Client
# from twilio.twiml.messaging_response import MessagingResponse
# import threading

# # ----------------------
# # Load Environment Variables
# # ----------------------
# load_dotenv()

# SENDER_EMAIL = os.getenv("SENDER_EMAIL")
# SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
# RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
# openai.api_key = os.getenv("OPENAI_API_KEY")
# PDF_PATH = "./Aibytec fine tuned data.pdf"
# WEBSITE_URL = "https://www.aibytec.com/"
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# # Initialize Twilio client
# twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# # Flask app for handling Twilio Webhooks
# app = Flask(__name__)

# # ----------------------
# # Functions
# # ----------------------

# # Function to send email
# def send_email(name, email, contact_no, area_of_interest):
#     subject = "New User Profile Submission"
#     body = f"""
#     New Student Profile Submitted:

#     Name: {name}
#     Email: {email}
#     Contact No.: {contact_no}
#     Area of Interest: {area_of_interest}
#     """
#     message = MIMEMultipart()
#     message['From'] = SENDER_EMAIL
#     message['To'] = RECEIVER_EMAIL
#     message['Subject'] = subject
#     message.attach(MIMEText(body, 'plain'))
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
#         server.quit()
#         st.success("Email sent successfully!")
#     except Exception as e:
#         st.error(f"Error sending email: {e}")

# # Function to extract PDF text
# def extract_pdf_text(file_path):
#     try:
#         reader = PdfReader(file_path)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text() + "\n"
#         return text
#     except Exception as e:
#         st.error(f"Error reading PDF: {e}")
#         return ""

# # Function to scrape website content
# def scrape_website(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, "html.parser")
#         return soup.get_text()
#     except Exception as e:
#         return f"Error scraping website: {e}"

# # Function to generate OpenAI response
# def chat_with_ai(user_question, website_text, pdf_text, chat_history):
#     combined_context = f"Website Content:\n{website_text}\n\nPDF Content:\n{pdf_text}"
#     messages = [{"role": "system", "content": "You are a helpful assistant. Use the provided content."}]
#     for entry in chat_history:
#         messages.append({"role": "user", "content": entry['user']})
#         messages.append({"role": "assistant", "content": entry['bot']})
#     messages.append({"role": "user", "content": f"{combined_context}\n\nQuestion: {user_question}"})

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             max_tokens=256,
#             temperature=0.7,
#             stream=False
#         )
#         return response['choices'][0]['message']['content']
#     except Exception as e:
#         return f"Error generating response: {e}"

# # Function to send WhatsApp message
# def send_whatsapp_message(to_number, message_body):
#     try:
#         twilio_client.messages.create(
#             from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
#             body=message_body,
#             to=f"whatsapp:{to_number}"
#         )
#     except Exception as e:
#         print(f"Error sending WhatsApp message: {e}")

# # Flask webhook to receive WhatsApp replies
# @app.route("/whatsapp", methods=["POST"])
# def whatsapp_webhook():
#     incoming_msg = request.values.get("Body", "").strip()
#     from_number = request.values.get("From", "").strip()
#     if incoming_msg and from_number:
#         # Add the reply to the chatbot's chat history
#         st.session_state['chat_history'].append({"user": f"WhatsApp ({from_number}): {incoming_msg}", "bot": ""})
#     return str(MessagingResponse())

# # ----------------------
# # Streamlit UI and App Logic
# # ----------------------

# st.set_page_config(page_title="Student Profile & AI Chatbot", layout="wide")

# # Start Flask app in a separate thread
# def run_flask():
#     app.run(port=5000)

# threading.Thread(target=run_flask, daemon=True).start()

# # Session State Initialization
# if "page" not in st.session_state:
#     st.session_state['page'] = 'form'
# if "chat_history" not in st.session_state:
#     st.session_state['chat_history'] = []

# # ----------------------
# # PAGE 1: User Info Form
# # ----------------------
# if st.session_state['page'] == 'form':

#     with st.form(key="user_form"):
#         name = st.text_input("Name")
#         email = st.text_input("Email")
#         contact_no = st.text_input("Contact No.")
#         area_of_interest = st.text_input("Area of Interest")
        
#         # Create two columns for buttons
#         col1, col2 = st.columns(2)
#         with col1:
#             submitted = st.form_submit_button("Proceed to Chat ")
#         with col2:
#             continue_chat = st.form_submit_button(" Skip and Join Chat")
        
#         if submitted:
#             if name and email and contact_no and area_of_interest:
#                 send_email(name, email, contact_no, area_of_interest)
#                 st.session_state['page'] = 'chat'
#                 st.rerun()
#             else:
#                 st.warning("Please fill out all fields.")
        
#         if continue_chat:
#             st.session_state['page'] = 'chat'
#             st.rerun()

# # ----------------------
# # PAGE 2: Chatbot Interface
# # ----------------------
# elif st.session_state['page'] == 'chat':
#     for entry in st.session_state['chat_history']:
#         if entry['user']:
#             st.markdown(f"**You:** {entry['user']}")
#         if entry['bot']:
#             st.markdown(f"**Bot:** {entry['bot']}")

#     pdf_text = extract_pdf_text(PDF_PATH) if os.path.exists(PDF_PATH) else "PDF file not found."
#     website_text = scrape_website(WEBSITE_URL)

#     user_input = st.chat_input("Type your question here...")
#     if user_input:
#         st.session_state['chat_history'].append({"user": user_input, "bot": ""})
#         bot_response = chat_with_ai(user_input, website_text, pdf_text, st.session_state['chat_history'])
#         st.session_state['chat_history'][-1]['bot'] = bot_response
#         send_whatsapp_message("+YourPhoneNumber", f"New visitor message: {user_input}")
#         st.rerun()








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
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

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
        twilio_client.messages.create(
            from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
            body=message_body,
            to=f"whatsapp:{to_number}"
        )
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

# ---------------------
# Twilio Webhook Handler
# ---------------------
class TwilioWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        data = {key: value for key, value in [pair.split('=') for pair in body.split('&')]}
        incoming_msg = data.get('Body', '')
        sender = data.get('From', '')

        # Generate a chatbot response
        bot_response = chat_with_ai(incoming_msg, scrape_website(WEBSITE_URL), extract_pdf_text(PDF_PATH), st.session_state.get('chat_history', []))
        st.session_state['chat_history'].append({"user": incoming_msg, "bot": bot_response})

        # Create Twilio response
        resp = MessagingResponse()
        resp.message(bot_response)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str(resp).encode('utf-8'))

# Start webhook server in a separate thread
def start_webhook_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, TwilioWebhookHandler)
    print("Starting webhook server on port 8000...")
    httpd.serve_forever()

webhook_thread = threading.Thread(target=start_webhook_server, daemon=True)
webhook_thread.start()

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
        send_whatsapp_message("+14155238886", "Test message from chatbot")
        st.session_state['chat_history'].append({"user": user_input, "bot": ""})
        bot_response = chat_with_ai(user_input, website_text, pdf_text, st.session_state['chat_history'])
        st.session_state['chat_history'][-1]['bot'] = bot_response
        send_whatsapp_message("+YourPhoneNumber", f"New visitor message: {user_input}")
        st.rerun()
