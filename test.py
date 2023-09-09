import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from docx2pdf import convert
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image

# Email configuration (replace with your own credentials)
sender_email = "cometcreativeconsulting@gmail.com"
sender_password = "udcoauicgjytqpld"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Function to create a PDF with the welcome message and image
def create_welcome_pdf(name):
    pdf_filename = f"Welcome_Letter_{name}.pdf"
    
    # Create a PDF with the message and image
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Add the image
    img = Image("img1.png", width=400, height=400)
    
    # Create content
    content = []
    content.append(img)
    content.append(MIMEText(f"Hi {name}!\n\nWelcome to the team!\n\nHope you have a good time!"))
    
    doc.build(content)
    
    return pdf_filename

def send_email(receiver_name, receiver_email):
    try:
        # Create the email content
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Welcome to the Team"

        # Convert the Word document to PDF
        convert("Letter Template.docx")

        # Attach the welcome PDF
        pdf_filename = create_welcome_pdf(receiver_name)
        pdf_attachment = MIMEApplication(open(pdf_filename, "rb").read())
        pdf_attachment.add_header("Content-Disposition", "attachment", filename=pdf_filename)
        msg.attach(pdf_attachment)

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        # Clean up temporary files
        os.remove(pdf_filename)
        os.remove("Letter Template.pdf")

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
