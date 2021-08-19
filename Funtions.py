import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
# conn = sqlite3.connect("ISU.db")
# c = conn.cursor()
# c.execute("CREATE TABLE IF NOT EXISTS ISU (Institue_Name text,User_Name text,Password text,File text,Email text)")
# conn.commit()
# c.execute("INSERT INTO ISU(Institue_Name,User_Name,Password,File) VALUES (?,?,?,?)",('SCI',"Ranuga","Password","gdhjghdf"))
# conn.commit()
# c.execute("SELECT * FROM ISU WHERE User_Name=? AND Password=?",('Ranuga',"Password"))
# print(c.fetchall()[0][0])
# Institue_Name,User_Name,Password,File
def send_email(to_email,subject,message):
    print(" > Sending Email....")
    email_user = 'go2ranuga@gmail.com'
    email_password = 'ranuga2008'
    email_send = to_email

    subject = subject

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_password
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login(email_user, email_password)

        server.sendmail(email_user, email_send, text)
        print(" > Gmail Sended......")
        server.quit()
    except:
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login(email_user, email_password)
        server.sendmail(email_user, email_send, msg.as_string())
        print(" > Email Sended....")
        server.quit()
