from django.core.mail import EmailMessage, EmailMultiAlternatives
from emailbox.models import InstantReplyModel

import requests

def send_email(email, subject, body):
    # subject = subject
    # body = body
    # to_email = [email.email_address]
    #
    # email_obj = EmailMessage(subject=subject, body=body, to=to_email)
    # print('email sent')
    # email_obj.send()


    subject = subject
    html_message = f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta http-equiv='X-UA-Compatible' content='IE=edge'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>Document</title></head><body><div><div style='background-color:#D7C0F5;height:200px;width:auto;top:-0px;'></div><center><div style='background-color:#ffffff;width:600px;margin:10px;margin-left:-500px;filter:drop-shadow(0px 4px 60px rgba(0,0,0,0.05000000074505806));left:243px;top:-125px;position:relative;padding-bottom: 20px;'><div><br><div style='font-size:40px;font-weight:700;'>{subject}</div><br><br><br><br><div style='text-align:left; font-size:22px;font-weight:700; margin-left: 15px; margin-right: 15px;'>{body}</div></div><img style='margin-top: 30px;'src='https://client-backendifyi.vercel.app/static/media/Backendifyi.375e5c7c14bf36ec30c6.png'></div></center></div></body></html>"
    image1_url = 'https://client-backendifyi.vercel.app/static/media/Backendifyi.375e5c7c14bf36ec30c6.png'
    image1_data = requests.get(image1_url).content
    email_message = EmailMultiAlternatives(subject, '', to=[email.email_address])
    email_message.attach_alternative(html_message, "text/html")

    # Attach the images to the email message
    email_message.attach('Backendifyi.png', image1_data, 'image/png')
    email_message.send()
    InstantReplyModel.objects.create(email=email, subject=subject, body=body)

def send_csv(csv_data):
    email = "kothawleprem@gmail.com"
    subject = 'Data Export'
    message = 'Please find attached the exported data.'
    to_emails = [email]  # Replace with recipient email(s)

    email = EmailMessage(subject=subject, body=message, to=to_emails)
    email.attach('data.csv', csv_data, 'text/csv')

    email.send()
