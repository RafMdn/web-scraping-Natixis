import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import EXPEDITEUR , PASSWORD , SMTP_PORT , SMTP_SERVER


# Envoyer des emails
def send_emails(liste_destinataires,liste_fichiers):
    # Objet du message
    objet = "mise à jour des produits douane"

    # Corps du message
    body = f""" mise à jour des produits de la douane, veuillez recevoir la nouvelle liste, 
    la liste des produits ajoutés et la liste des produits retirés en fichiers attachés
    """
    # Parcours de la liste des destinataires
    for destinataire in liste_destinataires:

        # Création d'un objet message
        msg = MIMEMultipart()
        msg['From'] = EXPEDITEUR
        msg['To'] = destinataire
        msg['Subject'] = objet

        # Attachement du corps du message
        msg.attach(MIMEText(body, 'plain'))
        # Liste des fichiers à attacher
        for file in liste_fichiers:

            with open(file, 'rb') as f:
    
                file_data = f.read()
                file_name = f.name

                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(file_data)
                encoders.encode_base64(attachment)

                attachment.add_header('Content-Disposition', 
                                    'attachment; filename='+file_name) 

                msg.attach(attachment)

        text = msg.as_string()

        # Connexion au serveur SMTP
        print("Connexion au serveur...")
        TIE_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        TIE_server.starttls()
        TIE_server.login(EXPEDITEUR, PASSWORD)
        print("Connexion réussie au serveur")
        print()

        # Envoi du message
        print(f"Envoi de l'email à : {destinataire}...")
        TIE_server.sendmail(EXPEDITEUR, destinataire, text)
        print(f"Email envoyé à : {destinataire}")
        print()

    # Fermeture de la connexion au serveur SMTP
    TIE_server.quit()

