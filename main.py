import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import os

phone = os.environ.get('PHONE')
plaisio_url = os.environ.get('PLAISIO_URL')
sms_api = os.environ.get('SMS_API')
sms_username = os.environ.get('SMS_USERNAME')
sms_password = os.environ.get('SMS_PASSWORD')


def send_sms(sender,receiver,message):
    url = sms_api

    # Set POST fields here
    post_fields = {	'username': sms_username,
                    'password': sms_password,
                    'to': receiver,
                    'from': sender,
                    'text': message,
                    'encoding': 'UTF8'
    }

    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()
    return json[:2]


page = requests.get(plaisio_url)

# get the status from the webpage
page = page.text
page = page.split('orderStatus":"')
page = page[1].split('","')
status = page[0]

# open the status file

f = open("status.txt","a+", encoding="utf-8")
# move file stream to the start of the file
f.seek(0)

old_status = f.read()


# write to file the new status
if old_status != status:
    print('writing to file...')
    f.truncate(0)
    f.write(status)
    send_sms('PLAISIO',phone,f'Αλλαγή κατάστασης παραγγελίας σε: {status}')


f.close()




