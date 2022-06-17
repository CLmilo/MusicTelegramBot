import socketserver
import http.server
import ssl
import json
import requests

def getResponse(user_input):
    return user_input

with open('.token') as file:
    list = file.readlines()
    TOKEN = list[0].rstrip("\n")
    file.close()

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        post_data = self.rfile.read(int(self.headers['Content-Length']))
        json_data = json.loads(post_data)

        chat_id = json_data['message']['from']['id']
        user_input = json_data['message']['text']

        bot_output = getResponse(user_input)

        url = "https://api.telegram.org/bot"+TOKEN+"/sendMessage"

        r = requests.post(url = url, params = {'chat_id' : chat_id, 'text' : bot_output})
        if r.status_code == 200:
            self.send_response(200)
            self.end_headers() 

    def do_GET(self):
        self.send_response(200)
        self.end_headers()