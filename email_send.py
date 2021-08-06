
import smtplib
from email.mime.text import MIMEText


def send_mail(email, name, password):
    from_email = "hackedraw159@gmail.com"
    from_password = "6263420714"
    to_email = email
    img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTntY3A8wM9MtyPqd13CaOdNriuNFh1rmHGOA&usqp=CAU"

    subject = "Attendance System : Login - OTP"
    message = "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' " \
              "content='width=device-width, initial-scale=1'><style>.box{margin: 1rem;width: auto;background-color: " \
              "black;padding: 1rem;border: aqua 5px solid;border-radius: 20px;color:white;box-shadow: 0 19px 38px " \
              "rgba(0,0,0,0.50), 0 15px 12px rgba(0,0,0,0.22);}body{color: white;background-color: white;}h2{" \
              "color: aqua;}</style></head><body><div class='container box'><div class='row'>" \
              "<div class='col'><h1 style='text-align: left'>Attendance System Using Face Recognition</h1></div>" \
              "<div class='col'><img src=%s class='img-fluid rounded'></div>" \
              "</div></div><section><div class='container'><div " \
              "class='box'><h1>Hi</h1><div><h2>%s ,</h2></div><p>Please use the OTP below to login to your " \
              "account.</p><h2>%s</h2><p>Please don't share your OTP with anyone, If this wasn't you, contact your " \
              "google support team.</p></div></div></section></body></html>" % (img, name, password)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)


send_mail('abhishekparmarjnv@gmail.com', 'Abhishek Parmar', 4571)