import logging, requests, json, html
from flask import Flask, request, jsonify, json, Blueprint, render_template, request, jsonify, redirect, url_for
# from maindoc import generate_document
import pprint as pp
import main as main
#from views import views

'''
    REMEMBER: Web are reverse API's that react to events 
    To expose your local server to the internet, you can use ngrok.
    
    [ngrok] takes your localhost and gives you a public URL that you can use to expose your local web server to the internet.
    First install ngrok by following the instructions on their website: https://ngrok.com/download
    Then run ngrok (torun) ngrok http http://localhost:8080
    https://dashboard.ngrok.com/
    
    Then Start Flask: 
    export FLASK_APP=app
    flask run
    
    -- USE 'STAR' FEATURE ON SERVICECHANNEL API TO TEST HOOKS --- 

'''
class StoreData:
    def __init__(self):
        self.data = None

    def store(self, value):
        self.data = value

    def retrieve(self):
        return self.data

class StoreTokens:
    def __init__(self):
        self.token = None

    def store(self, value):
        self.token = value
    def retrieve(self):
        return self.token

class TokenParser:
    def __init__(self, toParse):
        self.token_table = json.loads(toParse)
        self.access_token = self.token_table['access_token']
        self.refresh_token = self.token_table['refresh_token']

    def get_token_table(self):
        return self.token_table

    def get_access_token(self):
        return self.access_token

    def get_refresh_token(self):
        return self.refresh_token

storedata = StoreData()
storetokens = StoreTokens()

class OAuthClient:
    def __init__(self, tokenURL, auth_header, username, password):
        self.tokenURL = tokenURL
        self.auth_header = auth_header
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None

    def get_resp(self):
        headers = {
            'Authorization': self.auth_header,
            'Content-Type': "application/x-www-form-urlencoded"
        }

        payload = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password"
        }
        print("sending reqeust to ", self.tokenURL)
        # Send the POST request
        response = requests.post(self.tokenURL, headers=headers, data=payload)
        print("[+]\n", response.text)
        print("[+]\n", response.json)
        print("[+]\n", response.status_code)
        if response.status_code == 200:
            new_tokens = response.json()
            new_token_str = json.dumps(new_tokens, indent=4)
            self.access_token = new_tokens['access_token']
            self.refresh_token = new_tokens['refresh_token']

           ### SENDS TOKENS TO TOKEN PARSER
            T = TokenParser(new_token_str)
            T.access_token = self.access_token
            T.refresh_token = self.refresh_token

           # storedata.store(response.json())
            storetokens.store(new_tokens)  ## Stores Data

            print("[+]\n", response.text)
            print('[+] TOKEN: \n', self.access_token)
            print('[+] REFRESH TOKEN: \n', self.refresh_token)
            print('[+] EXPIRES IN \n', new_tokens['expires_in'])
        else:
            print(f"Failed to authenticate: {response.status_code} - {response.content}")
            print(response.reason)

    def get_access_token(self):
        return self.access_token

    def get_refresh_token(self):
        return self.refresh_token


url = 'http://localhost:5000/webhook'
tokenURL = "https://sb2login.servicechannel.com/oauth/token"
auth_header = "Basic UFIuMjA5ODQ1NzU5OC4yNkFBMkVFOS0xMTUwLTRDQzctOEU0Qi1ENzk2MUM3NDFBRDY6RjQ4RDcxRDItNEFEOS00RjQ0LUE0MTktRjMxMUFBMUNEQTk3"
client = OAuthClient(tokenURL, auth_header, "fuad@dedicatedglass.com", "Dedicated!234")

client.get_resp()
access_token = client.get_access_token()
refresh_token = client.get_refresh_token()


print("[+] ACCESS TOKEN: ", access_token)
print("[+] REFRESH TOKEN: ", refresh_token)

print("[+] STARTING FLASK: ")
logging.basicConfig(level=logging.DEBUG)


''' THIS IS USED TO CREATE A BLUEPRINT TEMPLATE FOR ROOT URL '''
app = Flask(__name__)

''' REGISTERING BLUEPRINTS '''
# app.register_blueprint(views, url_prefix="/web")

@app.route('/')
def api_root():
    data = storedata.retrieve()
    # Convert the Python dictionary to a pretty-printed JSON string
    pretty_json = json.dumps(data, indent=4)
    print("[!] Data: \n", pretty_json)
    # Escape the JSON string for HTML
    escaped_json = html.escape(pretty_json)

    # creates a simple HTML page to display the JSON data
    html_string = f"""
               <!DOCTYPE html>
           <html>
           <head>
               <title>JSON Display</title>
           </head>
           <body>
               <h1>JSON Data:</h1>
               <pre>{escaped_json}</pre>
           </body>
           </html>
       """

    # Write the HTML string to a file
    with open("json_display.html", "w") as f:
        f.write(html_string)


    return f' \n[REFRESH TOKEN]{refresh_token}\n {html_string}'
# @app.route('/web')
# def api_web():
#     return f'Welcome to the API '


''' HOOK IS CALLED WHEN API STATE CHANGES  '''
@app.route('/NotificationWebHooks', methods=['POST'])
def NotificationWebHooks():
    print("[!] NOTIFICATION WEBHOOKS\n\n")

    if request.method == 'POST':
        data = request.get_json()
        print("[!] Webhook Data\n", data)

        ## prettify and store data
        pp.pprint(data, compact=True)
        pretty_json_str = pp.pformat(data, compact=True).replace("'", '"')
        storedata.store(data)  ## Stores Data

       ## gets data from JSON, then writes to file, with unique ID
        id = data['Object']['Id']
        with open(f'inbound_wo{id}.json', 'w') as f:
            f.write(pretty_json_str)
        print("********************")

        # Convert the JSON string to a Python dictionary
     #   hashed_data = json.loads(data)
        print("++++++++++++++++++")

        return redirect(url_for('api_root'))
        #return 'success', 200
        # return jsonify({"status": "Success", "message": "Document generated successfully"}), 200
    client.get_resp()
    access_token_internal = client.get_access_token()
    refresh_token_internal = client.get_refresh_token()
    data = request.get_json()
    token = request.headers.get('Authorization')
    app.logger.error(access_token_internal)
    app.logger.error(refresh_token_internal)
    logging.debug("Access Token: %s", access_token_internal)
    logging.debug("Refresh Token: %s", refresh_token_internal)

    logging.debug(data)
    if not token:
        return redirect(url_for('api_root'))
      #  return jsonify({"status": "Error", "message": "No token provided"}), 401


    logging.debug("Webhook Data: %s", data)
    print("[!] Webhook Data\n", data)
    print("[!] Request Data \n", request.data)


    pp.pprint(data, compact=True) ## Pretty Print Data
    pretty_json_str = pp.pformat(data, compact=True).replace("'", '"')


    with open(f'webook.json', 'w') as f:
        f.write(pretty_json_str)

    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        print("[!] Data: ", data)
        return f" DATA RECEIVED, DUMPING {json.dump(request.json)}"

    return jsonify({"status": "Success", "message": "Document generated successfully"}), 200


''' SIMPLE PAGE TO DISPLAYS WEBHOOK (HTTML)'''


@app.route('/web')
def index():
    print("[!] Accessing Index Page\n\n")
    token2 = OAuthClient.get_access_token
    token = storetokens.retrieve()
    data = storedata.retrieve()
    # Convert the Python dictionary to a pretty-printed JSON string
    pretty_json = json.dumps(data, indent=4)
    print("[!] Data: \n", pretty_json)
    # Escape the JSON string for HTML
    escaped_json = html.escape(pretty_json)

    # creates a simple HTML page to display the JSON data
    html_string = f"""
            <!DOCTYPE html>
        <html>
        <head>
            <title>JSON Display</title>
        </head>
        <body>
            <h1>JSON Data:</h1>
            <pre>{escaped_json}</pre>
        </body>
        </html>
    """

    # Write the HTML string to a file
    with open("json_display.html", "w") as f:
        f.write(html_string)

    return render_template('index.html',
                           TITLE="WEBHOOK",
                           CONTENT=pretty_json,
                           TOKEN= token
                           )


''' 
    CREATES A DYNAMIC WEBPAGE THAT DISPLAYS (AND CHANGES) BASED OFF OF WHAT IS INSIDE OF URL 
    EXAMPLE: http://localhost:5000/web/web/change/1234
    WILL DISPLAY: 1234 IN TITLE 
'''


@app.route('/web/change/<string:ID>')
def pageByID(ID):
    return render_template("index.html",
                           TITLE=ID,
                           CONTENT="This is a webhook")


'''
    TAKES JSON DATA FROM WEBHOOK AND DISPLAYS IT ON THE PAGE
    JSONIFY IS USED TO RETURN A PYTHON DICT TO JSON FORMAT
    EXAMPLE: http://localhost:5000/web/jsonobj/ 
    WILL DISPLAY: JSON DATA IN BODY 
'''

@app.route('/web/jsonobj')
def jsonobj():
    data2 = storedata.retrieve()

    data = {"Action": "UPDATE",
         "EventType": "WorkOrderStarRemoved",
         "Object": {"Category": "REPAIR",
                    "Id": 275863375,
                    "LocationId": 2006301252,
                    "ProviderId": 2098457598,
                    "SubscriberId": 2014917340,
                    "Trade": "FACADE",
                    "UpdatedBy": {"AuthUserId": 38135,
                                  "Email": "fuad@dedicatedglass.com",
                                  "FullName": "",
                                  "Id": 4425509,
                                  "ProviderId": 2098457598,
                                  "UserName": "fuad@dedicatedglass.com"},
                    "UpdatedDate_DTO": "2024-04-26T19:09:06.6394621-04:00"},
         "Type": "WoRootNotification",
         "Version": 1}
    return jsonify(data2)

''' GETS INCOMING DATA FROM WEBHOOK AND DISPLAYS IT ON THE PAGE '''
@app.route("/data")
def get_data():
    data = request.get_json()
    return jsonify(data)

''' 
    PASSES A QUERY [?] PARAMATER TO THE URL 
    IT PULLS THE QUERY PARAMATER AND DISPLAYS IT ON THE PAGE
    EXAMPLE: http://localhost:5000/web/query?name=FUAD --- *refer: [?]name=FUAD)
    WILL DISPLAY: FUAD IN TITLE

    USAGE: 'args' is a dictionary that contains all the query parameters in the URL
'''


@app.route('/search/query')
def get_query_param():
    args = request.args
    id = request.args.get('TOKEN')
    return render_template("index.html",
                           TITLE=id,
                           CONTENT="This is a webhook")


if __name__ == '__main__':
    app.run(host="localhost", port=5005, debug=True)
