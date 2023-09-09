pip install -r requirements.txt

import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Email configuration (replace with your own credentials)
sender_email = "cometcreativeconsulting@gmail.com"
sender_password = "udcoauicgjytqpld"
smtp_server = "smtp.gmail.com"
smtp_port = 587

def send_email(receiver_name, receiver_email):
    try:
        # Create the email content
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Welcome to the Team"

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("Welcome Email Sender App")
receiver_name = st.text_input("Enter the name of the recipient:")
receiver_email = st.text_input("Enter the recipient's email:")

if st.button("Preview"):
    if receiver_name and receiver_email:
        st.image("img1.png", caption="Image Preview", use_column_width=True)
        st.write(f"Hi {receiver_name}!")
        st.write("Welcome to the team!")
        st.write("Hope you have a good time!")

if st.button("Send Welcome Email"):
    if receiver_name and receiver_email:
        result = send_email(receiver_name, receiver_email)
        if result is True:
            st.success("Welcome email sent successfully!")
        else:
            st.error(f"Failed to send the email. Error: {result}")
