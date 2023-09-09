import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import io
from reportlab.pdfgen import canvas

# Email configuration (replace with your own credentials)
sender_email = "cometcreativeconsulting@gmail.com"
sender_password = "udcoauicgjytqpld"
smtp_server = "smtp.gmail.com"
smtp_port = 587

def create_pdf(receiver_name):
    # Create a PDF with the same text as the email body
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, f"Hi {receiver_name},")
    c.drawString(100, 730, "This mail has been sent to you from the web app.")
    c.drawString(100, 710, "Have a good day!")
    c.save()
    buffer.seek(0)
    return buffer

def send_email(receiver_name, receiver_email):
    try:
        # Create the email content
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Web App Email"

        # Create the email body
        email_body = f"Hi {receiver_name},\n\nThis mail has been sent to you from the web app. Please check for attachment.\n\nHave a good day!"
        body = MIMEText(email_body, "plain")
        msg.attach(body)

        # Create the PDF
        pdf_buffer = create_pdf(receiver_name)

        # Attach the PDF
        pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
        pdf_attachment.add_header("Content-Disposition", "attachment", filename="mail_attachment.pdf")
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
st.title("Email Sender App v2")
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
