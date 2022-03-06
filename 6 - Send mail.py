#6 - Send Mail

username = "mail.prog.atlhe@gmail.com"
password = "passeword"
mail_from = "mail.prog.atlhe@gmail.com"

def send_mail(adresse_mail):
    recipients = [adresse_mail]
    msg = MIMEMultipart()
    msg['Subject'] = "Meilleures Performances en athlétisme sur le dernier mois"
    msg['From'] = 'mail.prog.atlhe@gmail.com'

    html = """\
            <html>
            <head></head>
            <body>
            <p>
                <br>Voici les meilleurs performances par épreuve en athlétisme sur les quatre dernières semaines :<br>
                <br><br>
                {0}
                <br>NB : ci-dessous le tableau avec les seuils pris en compte pour effectuer le tableau ci-dessus :<br>
                <br><br>
                {1}
                </p>
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
        server.sendmail(msg['From'], recipients , msg.as_string())
        server.close()
        
    except Exception as e:
            print("Error for connection: {}".format(e))

send_mail(give_mail)
