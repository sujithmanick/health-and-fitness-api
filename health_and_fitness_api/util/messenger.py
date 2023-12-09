import smtplib
from email.mime.text import MIMEText

def send_verification_email(app,name,email,link):
    try:
        smtp_ssl_host = app.config['SMTP_SSL_HOST']
        smtp_ssl_port = app.config['SMTP_SSL_PORT']
        sender_address = app.config['MAIL_SENDER_ADDRESS']
        sender_pass = app.config['MAIL_SENDER_PASSWORD']
        sender = app.config['MAIL_SENDER_ADDRESS']
        targets = email
        msg = MIMEText(f'Hi {name}\n\n Use this link to activate your health-and-fittness-account\n\n {link}')
        msg['Subject'] = 'New account verification | health-and-fittness-api'
        msg['From'] = sender
        msg['To'] = email

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(sender_address,sender_pass )
        server.sendmail(sender,targets,msg.as_string())
        server.quit()
    except Exception as e:
        print(e) 