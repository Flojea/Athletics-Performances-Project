#ETAPE 6 -> Mail -> newsletter 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

username = "athle.mois.pelletier@gmail.com"
password = "Pelletouz"
mail_from = "athle.mois.pelletier@gmail.com"
mail_to = "athle.mois.pelletier@gmail.com"

recipients = ['athle.mois.pelletier@gmail.com'] 
emaillist = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = "Meilleures Performances en athlétisme sur les derniers 30 jours"
msg['From'] = 'athle.mois.pelletier@gmail.com'

html = """\
        <html>
          <head></head>
          <body>
            {0}
          </body>
        </html>
""".format(df_mail.to_html(index=False))

part1 = MIMEText(html, 'html')
msg.attach(part1)

try:
    """Checking for connection errors"""

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('athle.mois.pelletier@gmail.com',password)
    server.sendmail(msg['From'], emaillist , msg.as_string())
    server.close()

except Exception as e:
    print("Error for connection: {}".format(e))
