#ETAPE 6 -> Mail -> newsletter 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

username = "mail.prog.atlhe@gmail.com"
password = "passeword"
mail_from = "mail.prog.atlhe@gmail.com"
mail_to = "jeandel.florian@gmail.com"

recipients = ['jeandel.florian@gmail.com'] 
emaillist = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = "Meilleures Performances en athlétisme sur les derniers 30 jours"
msg['From'] = 'mail.prog.atlhe@gmail.com'

html = """\
        <html>
          <head></head>
          <body>
            {0}
            {1}
          </body>
        </html>
""".format(df_mail.to_html(),df_seuil.to_html())

part1 = MIMEText(html, 'html')
msg.attach(part1)

try:
    """Checking for connection errors"""

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('mail.prog.atlhe@gmail.com',password)
    server.sendmail(msg['From'], emaillist , msg.as_string())
    server.close()

except Exception as e:
    print("Error for connection: {}".format(e))


