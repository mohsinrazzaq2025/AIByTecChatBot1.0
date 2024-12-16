import openai
import requests
from bs4 import BeautifulSoup
import pickle
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import fitz  # PyMuPDF for PDF text extraction
import streamlit as st

# Set OpenAI API key (Consider using environment variables for security)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Gmail credentials (use environment variables for security)
gmail_user = os.getenv("GMAIL_USER", "mohsin.razzaq2025@gmail.com")
gmail_password = os.getenv("GMAIL_PASSWORD")

# Website URL
url = "https://aibytec.com/"

# Fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all text from the webpage
website_text = ' '.join([p.get_text() for p in soup.find_all('p')])

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            pdf_text += page.get_text("text")
        return pdf_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Combine the website text and PDF text
pdf_text = extract_text_from_pdf("/Aibytec fine tuned data.pdf")
combined_context = website_text + "\n\n" + pdf_text  # Combine website and PDF data

# Function to send email notification
def send_email(name, email):
    try:
        subject = "New User Data from Aibytec Assistant"
        body = f"Name: {name}\nEmail: {email}"
        msg = MIMEMultipart()
        msg["From"] = gmail_user
        msg["To"] = gmail_user
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()

        print("Chatbot: User data sent to Gmail successfully!")
    except Exception as e:
        print(f"Chatbot: Failed to send email. Error: {e}")

# Function to generate answers using OpenAI
def generate_answer(query, context):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant with knowledge about the Aibytec website and the PDF document."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.0,
            max_tokens=200
        )
        answer = response.choices[0].message['content'].strip()
        return answer if answer else "I do not have this information."
    except Exception as e:
        print(f"Chatbot: An error occurred while generating a response: {e}")
        return "I do not have this information."

# Initialize user data storage
user_data_file = "user_data.pkl"

# Load existing user data if available
if os.path.exists(user_data_file):
    with open(user_data_file, "rb") as file:
        user_data = pickle.load(file)
else:
    user_data = {}

# Function to store user data persistently
def save_user_data(user_data):
    with open(user_data_file, "wb") as file:
        pickle.dump(user_data, file)

# Function for chatbot interaction and response
def chatbot_ui(user_input, user_name, user_email):
    # Store user data
    if user_name not in user_data:
        user_data[user_name] = {"email": user_email}
        save_user_data(user_data)
        # Send user data to Gmail
        send_email(user_name, user_email)

    # Generate response using combined context
    response = generate_answer(user_input, combined_context)
    return response

# # Streamlit UI
# def create_chatbot_interface():
#     st.title("Aibytec Assistant")

#     # User input fields for name and email
#     user_name = st.text_input("Your Name", placeholder="Enter your name here")
#     user_email = st.text_input("Your Email", placeholder="Enter your email address")

#     # User input for chat
#     user_query = st.text_area("Ask me anything about Aibytec", placeholder="Enter your question here")

#     # Button to submit the query
#     if st.button("Submit"):
#         if user_name and user_email and user_query:
#             response = chatbot_ui(user_query, user_name, user_email)
#             st.write(f"**Assistant:** {response}")
#         else:
#             st.warning("Please provide your name, email, and a question.")
import streamlit as st

# Simulated chatbot logic (replace with your actual function)
def chatbot_ui(user_input, user_name, user_email, chat_history):
    response = f"Hello {user_name}, you asked: '{user_input}'. This is a placeholder response."
    chat_history.append({"user": user_input, "bot": response})
    return chat_history

# Streamlit UI
def create_chatbot_interface():
    # Page title and description
    st.set_page_config(page_title="Aibytec Assistant", layout="wide")
    st.title("🤖 Aibytec Assistant")
    st.markdown("Welcome to the Aibytec Assistant! Ask me anything about the Aibytec website or related PDFs.")

    # Sidebar for user details
    st.sidebar.header("User Details")
    user_name = st.sidebar.text_input("Your Name", placeholder="Enter your name")
    user_email = st.sidebar.text_input("Your Email", placeholder="Enter your email")

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    st.subheader("Chat Interface")
    with st.container():
        # Display chat history
        for message in st.session_state["chat_history"]:
            st.markdown(f"**You:** {message['user']}")
            st.markdown(f"**Assistant:** {message['bot']}")

    # User input for chat
    user_query = st.text_input("Type your question below", placeholder="Enter your question here")

    # Submit and Reset Buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Submit"):
            if user_name and user_email and user_query:
                st.session_state["chat_history"] = chatbot_ui(
                    user_query, user_name, user_email, st.session_state["chat_history"]
                )
                st.experimental_rerun()  # Refresh to show updated chat
            else:
                st.warning("Please fill in all fields (Name, Email, and Question).")

    with col2:
        if st.button("Reset Chat"):
            st.session_state["chat_history"] = []
            st.experimental_rerun()

# Run the Streamlit app
if __name__ == "__main__":
    create_chatbot_interface()
