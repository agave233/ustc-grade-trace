# -*- coding: utf-8 -*-
import smtplib
import datetime
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
# _user = ""
# _pwd  = ""
# _to   = ""

def addimg(src,imgid):
    fp = open(src, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', imgid)
    return msgImage

def mail(HTMl,text,_user,_pwd,_to):
    msg = MIMEMultipart('related')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #text = text.decode("utf-8")
    HTML = HTMl
    msgtext = MIMEText(HTML, "html", "utf-8")
    msg.attach(msgtext)
    # msg.attach(addimg("captcha.jpg","weekly"))
    msg["Subject"] = text
    msg["From"] = _user
    msg["To"] = _to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print "Success!"
    except smtplib.SMTPException, e:
        print "Falied,%s" % e

