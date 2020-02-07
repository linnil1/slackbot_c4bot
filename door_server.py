from flask import Flask, request, jsonify
import os

import configuration

app = Flask(__name__)


@app.route("/door-open", methods=["POST"])
def doorOpen():
    if request.form.get('secret') == configuration.door_serect:
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})


# create certification if not exists
if not os.path.exists("data/self_key.pem"):
    os.system("openssl req -subj '/CN=localhost' -x509 -newkey rsa:2048 -nodes -days 365 -keyout data/self_key.pem -out data/self_cert.pem")
# main
app.run(host="0.0.0.0", port=12123,
        ssl_context=("data/self_cert.pem", "data/self_key.pem"),
        debug=True)
