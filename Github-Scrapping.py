import base64
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium import *
from dotenv import load_dotenv
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import csv


# Download the chrome web driver: https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.141/win64/chrome-win64.zip

# initialize the chrome driver:

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# For the Web Scrapping assignment I am taking Github.com
# Github credentials:

load_dotenv()

username = os.getenv('usn')
password = os.getenv('pass')

# directing to the Github login page:

driver.get("https://github.com/login")
response = requests.get('https://github.com/login', verify=True)

# find the username/email field and send the username itself to the input filed:

driver.find_element("id", "login_field").send_keys(username)

# find password input field and insert password also:

driver.find_element("id", "password").send_keys(password)

# cliok to login:

driver.find_element("name", "commit").click()

# wait for the ready state to be completed:

WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'"))
error_message = "Incorrect username or password"

# check for the login errors(if any):

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".flash-error"))
)

# to bypass the 2fa security and read the verification code automatically from the registered email:

SCOPES = ['https://mail.google.com/']
our_email = 'mradulgupta8306@gmail.com'


def gmail_authenticate():
    creds = None

    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # if there are no (valid) credentials availablle, let the user log in.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # save the credentials for the next run

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the Gmail API service


service = gmail_authenticate()


def get_emails(service):

    # Request a list of all the messages
    result = service.users().messages().list(userId='me', q='from: GitHub <noreply@github.com> subject:"[GitHub] Please verify your device"').execute()

    # messages is a list of dictionaries where each dictionary contains a message id.
    messages = result.get('messages')

    # If no messages found, return None
    if not messages:
        return None

    # Get the latest message
    msg = service.users().messages().get(
        userId='me', id=messages[0]['id']).execute()

    # Get value of 'payload' from dictionary 'txt'
    payload = msg['payload']
    headers = payload['headers']

    # Look for OTP in the body
    otp = None
    for part in payload.get('parts', []):
        body = part.get('body', {}).get('data', '')
        soup = BeautifulSoup(base64.urlsafe_b64decode(
            body + '==='), 'html.parser')
        strong_tag = soup.find('strong', {'style': 'letter-spacing: 24px;'})
        if strong_tag:
            otp = strong_tag.text.strip()
            break

    return otp


otp1 = get_emails(service)



# Data Extraction:

# lets get the information about the public repositories:

repos = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".js-repos-container")))

# Wait until the text is not "Loading..."

WebDriverWait(driver, 10).until(lambda x: repos.text != "Loading...")

# iterate over the repos and insert the urls of the repositories in a .csv file named 'Repositories.csv':
# "li.public" for public repositories and "li.private" for private repositories

repo_data=[]
for repo in repos.find_elements("css selector", "li.public"):
    url = repo.find_element("css selector", "a").get_attribute("href")
    repo_data.append((url))
     

# now writing it into a csv file:

with open('Repositories.csv', 'w', newline='') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(['Repository URL'])
    for url in repo_data:
        csvwriter.writerow([url])

