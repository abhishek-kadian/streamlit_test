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

def create_pdf_attachment(receiver_name):
    # Create a PDF file with the same text as the email body
    pdf_content = f"Hi {receiver_name},\n\nThis mail has been sent to you from the web app.\n\nHave a good day!"
    
    # Create a temporary PDF file
    pdf_filename = "temp_mail_attachment.pdf"
    with open(pdf_filename, "w") as pdf_file:
        pdf_file.write(pdf_content)
    
    # Create a MIMEApplication for the attachment
    pdf_attachment = MIMEApplication(open(pdf_filename, "rb").read())
    pdf_attachment.add_header("Content-Disposition", "attachment", filename="mail_attachment.pdf")
    
    # Clean up the temporary PDF file
    os.remove(pdf_filename)
    
    return pdf_attachment

def send_email(receiver_name, receiver_email):
    try:
        # Create the email content
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Web App Email"

        # Create the email body
        email_body = f"Hi {receiver_name},\n\nThis mail has been sent to you from the web app.\n\nHave a good day!"
        body = MIMEText(email_body, "plain")
        msg.attach(body)

        # Attach the PDF
        pdf_attachment = create_pdf_attachment(receiver_name)
        msg.attach(pdf_attachment)

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
