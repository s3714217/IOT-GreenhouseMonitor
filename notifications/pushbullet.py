import json
import logging
import requests

class Pushbullet:

    def __init__(self, token):
        self.__token = token

    '''
    Send a notification via Pushbullet with a title and body
    '''
    def send_note(self, title, body):
        logging.debug("Sending notification - Title: %s" % title)
        logging.debug("Sending notification - Body: %s" % body)

        data = { "type": "note", "title": title, "body": body }
        response = requests.post("https://api.pushbullet.com/v2/pushes", 
            data = json.dumps(data),
            headers = { 
                "Authorization": "Bearer " + self.__token, 
                "Content-Type": "application/json" 
            })

        if(response.status_code != 200):
            logging.error("Failed to send Pushbullet notification")
            raise Exception()

        logging.info("Notification sent.")