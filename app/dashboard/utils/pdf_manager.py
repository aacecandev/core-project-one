import base64
import re

import pdfkit
import streamlit as st
from bs4 import BeautifulSoup
from mailjet_rest import Client


def scrape_html_file():
    with open("./streamlit_raw.html") as f:
        html = f.read()

    return BeautifulSoup(html)


def write_pdf_to_disk(soup):
    with open("/app/streamlit.html", "w+") as f:
        f.write(str(soup))
        f.close()

    options = {
        "page-size": "A4",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
    }

    pdfkit.from_file("./streamlit.html", "./streamlit.pdf", options=options)


def create_pdf(victims_data):
    victims_average_list = [item[1] for item in victims_data["average"].items()]

    soup = scrape_html_file()

    for index, td in enumerate(soup.select("tbody > tr > td:nth-child(2)")):
        td.string = str(victims_average_list[index])

    write_pdf_to_disk(soup)


def email_validator(emai_address: str):
    if re.fullmatch(r"^[^@]+@[^@]+\.[^@]+$", emai_address):
        return True
    else:
        return False


def email_sender(email_address):
    with open("./streamlit.pdf", "rb") as pdf:
        data = pdf.read()

    pdf_enconded = base64.b64encode(data).decode()

    mailjet = Client(
        auth=(st.secrets["api_key"], st.secrets["api_secret"]), version="v3.1"
    )
    data = {
        "Messages": [
            {
                "From": {
                    "Email": st.secrets["sender_email"],
                    "Name": st.secrets["sender_name"],
                },
                "To": [
                    {
                        "Email": email_address,
                    }
                ],
                "Subject": "Core Project One Report",
                "TextPart": "Enjoy your report!",
                "Attachments": [
                    {
                        "ContentType": "application/pdf",
                        "Filename": "report.pdf",
                        "Base64Content": pdf_enconded,
                    }
                ],
            }
        ]
    }
    return mailjet.send.create(data=data)


def email_manager(email_address):
    try:
        if email_validator(email_address):
            sent = email_sender(email_address)
            if sent.status_code == 200:
                return "Success!"
            else:
                return "Error!"
        else:
            raise ValueError("Invalid email address")
    except ValueError as e:
        print(e)
        return "Invalid email address"
