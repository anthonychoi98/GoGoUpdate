from bs4 import BeautifulSoup
import requests
import time
import os
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

print 'What anime would you like for the next episode release to be notified of? : '
print 'Not case sensitive BUT MUST be spelled appears on GoGoAnime'
animetitle = raw_input()
print 'Would you like an email(e) or desktop(d) notification? e/d?'
method = raw_input()

if method == 'e':
	email = raw_input("Enter email address: ")
	password = raw_input('Enter password: ')

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

while True:

	r = requests.get('https://gogoanime.io')

	soup = BeautifulSoup(r.text, 'html.parser')

	results = soup.find_all('p',attrs={'class':'name'})
	episodes = soup.find_all('p', attrs={'class':'episode'})

	records= []

	i = 0
	for result in results:
		anime = result.find('a').text
		url = result.find('a')['href']
		url = 'https://gogoanime.io' + url
		latest_episode = episodes[i].text
		records.append((anime, url, latest_episode))
		i= i + 1

	i = 0
	found = 0
	for record in records:
		if animetitle.lower() == records[i][0].lower():
			#print 'New episode of Mob Psycho! ' + records[i][2]
			found = 1
			break
		i=i+1

	if found == 0:
		time.sleep(3)
		print 'Checking again...'
		continue

	if found == 1:
		if method == 'e':
			#message = 'Newest episode of ' + records[i][0] + ': ' + records[i][2] + ' Link: ' + records[i][1]
			subject = 'Newest episode of ' + records[i][0] + ' ' + records[i][2]
			html = records[i][1]

			messageHTML = '<p>Link to  <a href="https://gogoanime.io"> "GoGoAnime" <a> <p>'
			messagePlain = 'Link to new episode: '

			msg = MIMEMultipart('alternative')
			msg['From'] = email
			msg['To'] = email
			msg['Subject'] = subject

			msg.attach(MIMEText(messagePlain, 'plain'))
			msg.attach(MIMEText(messageHTML, 'html'))

			content = str(records[i][1]) + "hello"

			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(email, password)
			text = msg.as_string()
			server.sendmail('gogoupdate@gmail.com', email , text)
			server.quit()
			break
		elif method == 'd':
			notify(records[i][0], 'Newest Episode : ' + records[i][2])
			break
	break

	







