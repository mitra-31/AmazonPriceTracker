import smtplib
import os



def sendNotification(link,reciverid):
    
    mailid = 'pavan.pushyamitra99@gmail.com'
    key = os.getenv("AUTH_KEY")
    
    server = smtplib.SMTP('smpt.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login(mailid ,key)
    
    subject = "Price Fell Down !!!"
    
    body = "<h4> Check the amazon link </h4>" + link
    
    message = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(mailid,reciverid,message)
    
    server.quit()
    
    