#!/usr/bin/env python
# coding: utf-8

# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

import smtplib
import time
import csv

from config import smtp_host, smtp_user, smtp_passwd


plain = """Caro {nome},

Grazie per aver partecipato alla prima serata del corso "Introduzione a Python".

Ti ringraziamo anche per aver contribuito, tramite la tua iscrizione e partecipazione all'Associazione, a continuare a promuovere e diffondere la cultura del software Libero e dell'Open Source!

Tramite il link potrai scaricare del materiale omaggio offerto dal BgLUG per permetterti di approfondire individualmente qualche utilizzo particolare del linguaggio Python.

Ti ricordiamo che il BgLUG si incontra ogni mercoledì sera per discutere liberamente e confrontarsi su qualsiasi argomento inerente - o correlato - al software Libero ed Open Source. Chiunque abbia bisogno di una mano, abbia domande, curiosità o semplicemente voglia arricchire la serata con qualche argomento è sempre il benvenuto. Più siamo e meglio è!

Il tuo link personale per scaricare gli e-books da humblebundle è: {codice}


Alla prossima!

-- 
Staff BgLUG
Bergamo Linux Users Group <http://bglug.it/>
"""


html = """<p>Caro {nome},<br></p>

<p>Grazie per aver partecipato alla prima serata del corso "Introduzione a Python".<br></p>

<p>Ti ringraziamo anche per aver contribuito, tramite la tua iscrizione e partecipazione all'Associazione, a continuare a promuovere e diffondere la cultura del software Libero e dell'Open Source!<br></p>

<p>Tramite il link potrai scaricare del materiale omaggio offerto dal BgLUG per permetterti di approfondire individualmente qualche utilizzo particolare del linguaggio Python.<br></p>

<p>Ti ricordiamo che il BgLUG si incontra ogni mercoledì sera per discutere liberamente e confrontarsi su qualsiasi argomento inerente - o correlato - al software Libero ed Open Source. Chiunque abbia bisogno di una mano, abbia domande, curiosità o semplicemente voglia arricchire la serata con qualche argomento è sempre il benvenuto. <b>Più siamo e meglio è!</b><br></p>

<div style="text-align:center"><br><img src="cid:image1" width="412" height="189"><br><br></div>

<p>Il tuo link personale per scaricare gli e-books da humblebundle è: <a href={codice}>{codice}</a><br></p>

<p><br>Alla prossima!<br></p>

<p>-- <br>
Staff BgLUG<br>
Bergamo Linux Users Group (<a href="https://bglug.it">https://bglug.it</a>)<br></p>
"""


def send(nome, email, codice):

    strFrom = 'info@bglug.it'
    strTo = email
    subject = 'BgLUG: e-books omaggio per la partecipazione al corso "Introduzione a Python"!'

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = subject

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText(plain.format(nome=nome, codice=codice))
    msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(html.format(nome=nome, codice=codice), 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('python.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # Send the email (this example assumes SMTP authentication is required)
    smtp = smtplib.SMTP()
    smtp.connect(smtp_host)
    smtp.login(smtp_user, smtp_passwd)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()


if __name__ == '__main__':

    with open('recipients.csv') as fp:
        for line in csv.DictReader(fp):
            if line['email']:
                print 'sending to %s ...' % line['email'],
                send(line['nome'], line['email'], line['codice'])
                print 'OK'
                time.sleep(2)
