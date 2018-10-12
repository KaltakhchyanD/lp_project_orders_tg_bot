from email.message import EmailMessage
import smtplib
import os


def send_mail(txt_2_send, dst):
    src = os.getenv('EMAIL_FROM')
    pswd = os.getenv('PSWD')
    s = smtplib.SMTP('smtp.yandex.ru', 587)
    s.starttls()
    s.login(src, pswd)
    msg = EmailMessage()
    msg.set_content(txt_2_send)
    msg['Subject'] = 'New order'
    msg['From'] = src
    msg['To'] = dst
    s.send_message(msg)
    s.quit()