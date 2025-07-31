
from langchain_community.utilities import GoogleSerperAPIWrapper
from sendgrid.helpers.mail import To, Email, Content,Mail
import sendgrid
from langchain_core.tools import tool
from langchain.agents import Tool
import os

@tool
def send_email(subjectContent:str,description:str):
    """Send an email using SendGrid with a subject and HTML content."""
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("pharshana719@gmail.com")
    to_email = To("kasunkalharaweather@gmail.com")
    subject = subjectContent
    content = Content("text/html",description)
    mail = Mail(from_email,to_email,subject,content)
    response = sg.client.mail.send.post(request_body= mail.get())
    print(response.status_code)
    print(response.body)