import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from docx import Document  # Library to work with .docx files
from reportlab.pdfgen import canvas  # Library for creating PDFs

# Email configuration (replace with your own credentials)
sender_email = "cometcreativeconsulting@gmail.com"
sender_password = "udcoauicgjytqpld"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Function to create a PDF with the welcome message
def create_welcome_pdf(name):
    pdf_filename = f"Welcome_Letter_{name}.pdf"

    # Create a PDF with the message
    c = canvas.Canvas(pdf_filename)
    c.drawString(100, 750, "Hi!")
    c.drawString(100, 730, "Welcome to the team!")
    c.drawString(100, 710, "Hope you have a good time!")
    c.save()

    return pdf_filename

def send_email(receiver_name, receiver_email):
    try:
        # Create the email content
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Welcome to the Team"

        # Create the welcome PDF
        welcome_pdf = create_welcome_pdf(receiver_name)

        # Attach the welcome PDF
        pdf_attachment = MIMEApplication(open(welcome_pdf, "rb").read())
        pdf_attachment.add_header("Content-Disposition", "attachment", filename=welcome_pdf)
        msg.attach(pdf_attachment)

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        # Clean up temporary files
        os.remove(welcome_pdf)

        return True
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("Welcome Email Sender App")
receiver_name = st.text_input("Enter the name of the recipient:")
receiver_email = st.text_input("Enter the recipient's email:")

if st.button("Send Welcome Email"):
    if receiver_name and receiver_email:
        result = send_email(receiver_name, receiver_email)
        if result is True:
            st.success("Welcome email sent successfully!")
        else:
            st.error(f"Failed to send the email. Error: {result}")
