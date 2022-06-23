import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

import time
import streamlit as st
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)


url = "https://duckduckgo.com/"
SENDGRID_API_KEY = ""


firefoxOptions = Options()
firefoxOptions.add_argument("--headless")
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(
    options=firefoxOptions,
    service=service,
)


#streamlit
def interface():
    st.title("Interface de test minimale") 
   
    #selenium
    if st.button("url de test"):
        driver.get(url)

    #téléchargement sur dossier local
    #fichier_test = st.file_uploader("Choisir un fichier")
    fichier_test = st.text_input("Entrez le nom de votre fichier")
    
    mail = st.text_input("Entrez une adresse pour envoyer un mail test")
    if "@" in mail:
        if st.button("envoyer un mail de test"):
            envoi_mail(mail, fichier_test)
            
    if st.button("Test de téléchargement"):
        telecharge_test("/")

    if st.button("Liste les fichiers locaux"):
        st.write(os.listdir())
        print(os.listdir())
            

#envoi mail
def envoi_mail(mail_principal, fichier):
    message = Mail(
        from_email='as.mailsystem@gmail.com',
        to_emails= mail_principal,
        subject='Mail de test',
        html_content='<strong>Test de mail </strong>')
    
    with open(fichier, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(fichier),
        FileType('application/xlsx'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    return response


def telecharge_test(dossier_telecharge):
    url_test = 'https://notice-utilisation.net/mode-demploi-blackberry-9720/'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
                    "download.default_directory": dossier_telecharge, #Change default directory for downloads
                    "download.prompt_for_download": False, # Téléchargement automatique si False
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True # N'ouvre pas le pdf dans Chrome si True
                    })

    driver = webdriver.Chrome(options=options)
    driver.get(url_test)
    time.sleep(3)
    xpath = "/html/body/div[1]/div/article/div/div/div[1]/div/div[3]/a"
    bouton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))
    print("boutonnnnn!")
    bouton.click()
    time.sleep(2)
    

interface()