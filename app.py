# import openai
# import requests
# from bs4 import BeautifulSoup
# import pickle
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import fitz  # PyMuPDF for PDF text extraction
# import streamlit as st

# # Set OpenAI API key (Consider using environment variables for security)
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Gmail credentials (use environment variables for security)
# gmail_user = os.getenv("GMAIL_USER", "mohsin.razzaq2025@gmail.com")
# gmail_password = os.getenv("GMAIL_PASSWORD")

# # Website URL
# url = "https://aibytec.com/"

# # Fetch the webpage content
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

# # Extract all text from the webpage
# website_text = ' '.join([p.get_text() for p in soup.find_all('p')])

# # Extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     pdf_text = ""
#     try:
#         doc = fitz.open(pdf_path)
#         for page in doc:
#             pdf_text += page.get_text("text")
#         return pdf_text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ""

# # Combine the website text and PDF text
# pdf_text = extract_text_from_pdf("Aibytec fine tuned data.pdf")# pdf_text = extract_text_from_pdf("./Aibytec fine tuned data.pdf")
# combined_context = website_text + "\n\n" + pdf_text  # Combine website and PDF data

# # # Function to send email notification
# # def send_email(name, email):
# #     try:
# #         subject = "New User Data from Aibytec Assistant"
# #         body = f"Name: {name}\nEmail: {email}"
# #         msg = MIMEMultipart()
# #         msg["From"] = gmail_user
# #         msg["To"] = gmail_user
# #         msg["Subject"] = subject
# #         msg.attach(MIMEText(body, "plain"))

# #         # Connect to Gmail SMTP server
# #         server = smtplib.SMTP("smtp.gmail.com", 587)
# #         server.starttls()
# #         server.login(gmail_user, gmail_password)
# #         server.send_message(msg)
# #         server.quit()

# #         print("Chatbot: User data sent to Gmail successfully!")
# #     except Exception as e:
# #         print(f"Chatbot: Failed to send email. Error: {e}")
# def send_email(name, email):
#     try:
#         subject = "New User Data from Aibytec Assistant"
#         body = f"Name: {name}\nEmail: {email}"
#         msg = MIMEMultipart()
#         msg["From"] = gmail_user
#         msg["To"] = gmail_user
#         msg["Subject"] = subject
#         msg.attach(MIMEText(body, "plain"))

#         # Connect to Gmail SMTP server
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(gmail_user, gmail_password)
#         server.send_message(msg)
#         server.quit()

#         print("Chatbot: User data sent to Gmail successfully!")
#     except smtplib.SMTPAuthenticationError as e:
#         print("Chatbot: Authentication failed - check your Gmail credentials.")
#         print(e)
#     except Exception as e:
#         print(f"Chatbot: Failed to send email. Error: {e}")


# # Function to generate answers using OpenAI
# def generate_answer(query, context):
#     try:
#         messages = [
#             {"role": "system", "content": "You are a helpful assistant with knowledge about the Aibytec website and the PDF document."},
#             {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
#         ]

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             temperature=0.0,
#             max_tokens=200
#         )
#         answer = response.choices[0].message['content'].strip()
#         return answer if answer else "I do not have this information."
#     except Exception as e:
#         print(f"Chatbot: An error occurred while generating a response: {e}")
#         return "I do not have this information."

# # Initialize user data storage
# user_data_file = "user_data.pkl"

# # Load existing user data if available
# if os.path.exists(user_data_file):
#     with open(user_data_file, "rb") as file:
#         user_data = pickle.load(file)
# else:
#     user_data = {}

# # Function to store user data persistently
# def save_user_data(user_data):
#     with open(user_data_file, "wb") as file:
#         pickle.dump(user_data, file)

# # Function for chatbot interaction and response
# def chatbot_ui(user_input, user_name, user_email):
#     # Store user data
#     if user_name not in user_data:
#         user_data[user_name] = {"email": user_email}
#         save_user_data(user_data)
#         # Send user data to Gmail
#         send_email(user_name, user_email)

#     # Generate response using combined context
#     response = generate_answer(user_input, combined_context)
#     return response

# # # Streamlit UI
# # def create_chatbot_interface():
# #     st.title("Aibytec Assistant")

# #     # User input fields for name and email
# #     user_name = st.text_input("Your Name", placeholder="Enter your name here")
# #     user_email = st.text_input("Your Email", placeholder="Enter your email address")

# #     # User input for chat
# #     user_query = st.text_area("Ask me anything about Aibytec", placeholder="Enter your question here")

# #     # Button to submit the query
# #     if st.button("Submit"):
# #         if user_name and user_email and user_query:
# #             response = chatbot_ui(user_query, user_name, user_email)
# #             st.write(f"**Assistant:** {response}")
# #         else:
# #             st.warning("Please provide your name, email, and a question.")
# # Streamlit UI


# # def create_chatbot_interface():
# #     # Page setup
# #     st.set_page_config(page_title="Aibytec Assistant", layout="wide")
# #     st.title("🤖 Aibytec Assistant")
# #     st.markdown("Ask me anything about Aibytec!")

# #     # Sidebar for user details
# #     user_name = st.sidebar.text_input("Your Name", placeholder="Enter your name")
# #     user_email = st.sidebar.text_input("Your Email", placeholder="Enter your email")

# #     # Chat history initialization
# #     if "chat_history" not in st.session_state:
# #         st.session_state["chat_history"] = []

# #     # Display chat history
# #     st.subheader("Chat Interface")
# #     for chat in st.session_state["chat_history"]:
# #         st.markdown(f"**You:** {chat['user']}")
# #         st.markdown(f"**Assistant:** {chat['bot']}")

# #     # User input
# #     user_query = st.text_area("Type your question below", placeholder="Ask your question...")

# #     # Submit Button
# #     if st.button("Submit"):
# #         if user_name and user_email and user_query:
# #             # Simulate bot response for now
# #             bot_response = chatbot_ui(user_query, user_name, user_email) #f"Hello {user_name}, this is a placeholder response to: '{user_query}'"
# #             st.session_state["chat_history"].append({"user": user_query, "bot": bot_response})
# #         else:
# #             st.warning("Please fill in your name, email, and query.")

# #     # Reset Button
# #     if st.button("Reset Chat"):
# #         st.session_state["chat_history"] = []

# # 2
# def create_chatbot_interface():
#     # Page setup
#     st.set_page_config(page_title="Aibytec Assistant", layout="wide")
#     st.title("🤖 Aibytec Assistant")
#     st.markdown("Ask me anything about Aibytec!")

#     # Sidebar for user details
#     user_name = st.sidebar.text_input("Your Name", placeholder="Enter your name")
#     user_email = st.sidebar.text_input("Your Email", placeholder="Enter your email")

#     # Chat history initialization
#     if "chat_history" not in st.session_state:
#         st.session_state["chat_history"] = []

#     # User input
#     user_query = st.text_area("Type your question below", placeholder="Ask your question...")

#     # Submit Button
#     if st.button("Submit"):
#         if user_name and user_email and user_query:
#             # Get chatbot response
#             bot_response = chatbot_ui(user_query, user_name, user_email)
            
#             # Update chat history in session state
#             st.session_state["chat_history"].append({"user": user_query, "bot": bot_response})
            
#             # Clear the input area after submission
#             st.experimental_set_query_params()

#         else:
#             st.warning("Please fill in your name, email, and query.")

#     # Display chat history
#     st.subheader("Chat Interface")
#     for chat in st.session_state["chat_history"]:
#         st.markdown(f"**You:** {chat['user']}")
#         st.markdown(f"**Assistant:** {chat['bot']}")

#     # Reset Button
#     if st.button("Reset Chat"):
#         st.session_state["chat_history"] = []
#         st.session_state.clear()




# # Run the Streamlit app
# if __name__ == "__main__":
#     create_chatbot_interface()











# 2 page display
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
pdf_text = extract_text_from_pdf("Aibytec fine tuned data.pdf")  # Update this path
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
    except smtplib.SMTPAuthenticationError as e:
        print("Chatbot: Authentication failed - check your Gmail credentials.")
        print(e)
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

# Streamlit UI
def create_chatbot_interface():
    # Page setup
    st.set_page_config(page_title="Aibytec Assistant", layout="wide")
    
    # Step 1: User Info Collection
    if "user_info_submitted" not in st.session_state:
        st.title("Step 1: Provide Your Info")
        user_name = st.text_input("Your Name", placeholder="Enter your name here")
        user_email = st.text_input("Your Email", placeholder="Enter your email address")

        if st.button("Submit"):
            if user_name and user_email:
                st.session_state.user_info_submitted = True
                st.session_state.user_name = user_name
                st.session_state.user_email = user_email
                send_email(user_name, user_email)  # Send email
                st.success("Thank you! Your information has been submitted.")
                st.session_state.page = "chatbot"  # Mark that the user is ready for the chatbot
            else:
                st.warning("Please provide your name and email.")
    
    # Step 2: Chatbot Interface
    if st.session_state.get("page") == "chatbot":
        st.title("Step 2: Chat with Aibytec Assistant")
        st.markdown("Ask me anything about Aibytec!")

        # Display chat history
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        for chat in st.session_state["chat_history"]:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Assistant:** {chat['bot']}")

        user_query = st.text_area("Type your question below", placeholder="Ask your question...")

        if st.button("Submit"):
            if user_query:
                response = chatbot_ui(user_query, st.session_state.user_name, st.session_state.user_email)
                st.session_state["chat_history"].append({"user": user_query, "bot": response})
            else:
                st.warning("Please enter a question.")

        # Reset Button
        if st.button("Reset Chat"):
            st.session_state["chat_history"] = []

# Run the Streamlit app
if __name__ == "__main__":
    create_chatbot_interface()

