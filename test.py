import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Email configuration (replace with your own credentials)
sender_email = "cometcreativeconsulting@gmail.com"
sender_password = "Abhishek13"
smtp_server = "smtp.gmail.com"
smtp_port = 587

def send_email(receiver_name, receiver_email):
    try:
        # Create the email content
        message = MIMEText(f"Hi {receiver_name},\n\nThis mail has been sent to you from the web app.\n\nHave a good day!")
        message["Subject"] = "Web App Email"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("Email Sender App")
receiver_name = st.text_input("Enter the name of the recipient:")
receiver_email = st.text_input("Enter the recipient's email:")

if st.button("Preview"):
    if receiver_name and receiver_email:
        st.write(f"Preview Message:\n\nHi {receiver_name},\n\nThis mail has been sent to you from the web app.\n\nHave a good day!")

if st.button("Send Email"):
    if receiver_name and receiver_email:
        result = send_email(receiver_name, receiver_email)
        if result is True:
            st.success("Email sent successfully!")
        else:
            st.error(f"Failed to send the email. Error: {result}")
