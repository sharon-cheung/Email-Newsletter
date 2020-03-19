# newsproject.py

# Import the required libraries
import requests
import json
from datetime import datetime
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import charset

# Set up utf-8 encoding
charset.add_charset('utf-8',
                    charset.QP,
                    charset.QP,
                    'utf-8')

# Get sender credentials, APIkey, and a spreadsheet with the mailing list
sender_email = open('sender_email.txt', 'r')
sender_email = sender_email.read()

password = open('password.txt', 'r')
password = password.read()

key = open('apikey.txt', 'r')
key = key.read()

client_summary = pd.read_csv('client_summary.txt',
                             sep='\t')

# Form the URL query based the mailing list
def query_builder(client_table):
    url_container = []
    sort_method = 'sortBy=popularity&'
    num_clients = len(client_table)
    
    for i in range(0, num_clients):
        curr_client = client_table.iloc[i,:]
        
        if curr_client['News'] == True:
            url = 'https://newsapi.org/v2/top-headlines?'
            
            lang = curr_client['Language']
            country = curr_client['Country']
            q = curr_client['Query']
            category = curr_client['Category']
            source = curr_client['Source']

            if q != False and q !='FALSE':
                url = url + 'q={0}&' .format(q)
                
            if lang != False and lang !='FALSE':
                url = url + 'language={0}&' .format(lang)
                
            if country != False and country != 'FALSE':
                url = url + 'country={0}&' .format(country)
                
            if category != False and category !='FALSE':
                url = url + 'category={0}&' .format(category)
                
            if source !=False and source !='FALSE':
                url = url + 'source={0}&' .format(source)
            
            url = url + sort_method + "apiKey=" + key
            url_container.append(url)
        
        else: 
            url = ""
            url_container.append(url)
            
    return url_container

# Pull news articles from the api by the URL
# and output articles into an email body as a string
def show_news(url):
    response = requests.get(url)
    json_data = json.loads(response.text)
    articles = json_data.get('articles')
    num_articles = 0
    body = u""
    for item in articles:
        title = item.get('title')
        url = item.get('url')
        date = str(datetime.strptime(item.get('publishedAt')[0:10],
                                     '%Y-%m-%d').date()) # format the date
        body = body + '({0}) {1} \n {2} \n\n' .format(date, title, url)
        num_articles = num_articles + 1
    body = body + "\nNumber of Articles: {0}" .format(num_articles)
    return body

# Send the email to a recipient with news from url
def send_email(receiver_email, receiver, url):  
    message = MIMEMultipart()
    subject = "{0}'s News Summary" .format(receiver)
    
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    # Define the greeting for the email
    body = u"Hi {0}, here is your news summary:\n\n" .format(receiver)
    
    # Fill the email with news articles
    body = body + show_news(url)
    
    # Send the email
    message.attach(MIMEText(body,'plain','UTF-8'))
    text = message.as_string().encode('ascii')
    session = smtplib.SMTP('smtp.gmail.com: 587')
    session.starttls()
    session.login(sender_email, password)
    session.sendmail(sender_email,
                     receiver_email,
                     text)
    session.quit()

# Send emails to clients
def execute(client_table):
    client_table['URL'] = query_builder(client_table)
    num_clients = len(client_table)

    for i in range(0, num_clients):
        curr_client = client_table.iloc[i,:]
        
        if curr_client['News'] == True:
            send_email(curr_client['Email'],
                       curr_client['Name'],
                       curr_client['URL'])

# Sends the email
execute(client_summary)
