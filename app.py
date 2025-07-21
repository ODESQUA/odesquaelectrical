
from flask import Flask, request, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__, static_folder='.', static_url_path='')

GMAIL_USER_1 = os.getenv('GMAIL_USER_1')
GMAIL_PASS_1 = os.getenv('GMAIL_PASS_1')
GMAIL_USER_2 = os.getenv('GMAIL_USER_2')
GMAIL_PASS_2 = os.getenv('GMAIL_PASS_2')

def send_alert_email(subject, message):
    recipients = [GMAIL_USER_1, GMAIL_USER_2]
    for i, user in enumerate(recipients):
        password = GMAIL_PASS_1 if i == 0 else GMAIL_PASS_2
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(user, password)
            email_msg = MIMEMultipart()
            email_msg['From'] = user
            email_msg['To'] = user
            email_msg['Subject'] = subject
            email_msg.attach(MIMEText(message, 'plain'))
            server.sendmail(user, user, email_msg.as_string())
            server.quit()
            print(f"Alert sent to {user}")
        except Exception as e:
            print(f"Failed to send alert to {user}: {e}")

@app.route('/<path:path>', methods=['GET', 'POST'])
def static_proxy(path):
    if request.method == 'POST':
        send_alert_email("🚨 ALERT: Suspicious Activity Detected",
                         f"Someone attempted a POST to {path}\nIP: {request.remote_addr}")
    return send_from_directory(app.static_folder, path)

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        send_alert_email("🚨 ALERT: Suspicious Activity Detected",
                         f"Someone attempted a POST to the root URL\nIP: {request.remote_addr}")
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
