from flask import Flask, Response, request
from datetime import datetime
import json
from contact_resource import ContactResource
from flask_cors import CORS

import requests

# Create the Flask application object.
app = Flask(__name__)

CORS(app)

user_base_url = 'http://6156usermicroservicetest-env.eba-ppxt22vh.us-east-1.elasticbeanstalk.com'
contacts_base_url = '54.242.126.44:5011'


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Contact-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/composite/id/<uid>", methods=["GET"])
def get_composite_by_uid(uid):

    user_url = user_base_url + "/api/user/id/"+ uid
    response = requests.get(user_url)

    if response.status_code != 200:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        return rsp

    user = response.json()

    contacts_url = contacts_base_url + "/api/contacts/id/"+uid
    response = requests.get(contacts_url)

    if response.status_code != 200:
        rsp = Response("NOT FOUND", status=response.status_code, content_type="text/plain")
        return rsp

    contact = response.json()

    result = {
        "uid": user.uid,
        "last_name": user.last_name,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "username": user.username,
        "contacts": contact
    }

    rsp = Response(json.dumps(result), status=200, content_type="application.json")

    return rsp


@app.route("/api/contacts/create/<uid>/<lname>/<fname>/<mname>/<username>/<email>/<e_type>/<phone>/<p_type>/<addr>/<a_type>", methods=["POST"])
def create_contacts_by_uid(uid, lname, fname, mname, username, email, e_type, phone, p_type, addr, a_type):

    user_url = user_base_url + "/api/users/create/"+uid+"/"+lname+"/"+fname+"/"+mname+"/"+username
    response = requests.post(user_url)

    if response.status_code != 200:
        rsp = Response("NOT FOUND", status=response.status_code, content_type="text/plain")
        return rsp
    
    contact_url = contacts_base_url + "/api/contacts/create/uid"
    if email != "NaN":
        url = contact_url + "/email/" + email + "/" + e_type
        response = requests.post(url)

        if response.status_code != 200:
            rsp = Response("NOT FOUND", status=response.status_code, content_type="text/plain")
            return rsp

    if phone != "NaN":
        url = contact_url + "/phone/" + phone + "/" + p_type
        response = requests.post(url)

        if response.status_code != 200:
            rsp = Response("NOT FOUND", status=response.status_code, content_type="text/plain")
            return rsp 

    if addr != "NaN":
        url = contact_url + "/addresse/" + addr + "/" + a_type
        response = requests.post(url)

        if response.status_code != 200:
            rsp = Response("NOT FOUND", status=response.status_code, content_type="text/plain")
            return rsp

    result = {
        "msg": "sucess"
    }
    rsp = Response(json.dumps(result), status=200, content_type="application.json")

    return rsp

# @app.route("/api/contacts/update/<uid>/<type>/<contact>/<kind>", methods=["PUT"])
# def update_contacts_by_uid(uid, type, contact, kind):

#     result = ContactResource.update_by_key(uid, type, contact, kind)

#     if result:
#         rsp = Response(json.dumps(result), status=200, content_type="application.json")
#     else:
#         rsp = Response("NOT FOUND", status=404, content_type="text/plain")

#     return rsp

# @app.route("/api/contacts/delete/<uid>/<type>/<kind>", methods=["DELETE"])
# def delete_contacts_by_uid(uid, type, kind):

#     result = ContactResource.delete_by_key(uid, type, kind)

#     if result:
#         rsp = Response(json.dumps(result), status=200, content_type="application.json")
#     else:
#         rsp = Response("NOT FOUND", status=404, content_type="text/plain")

#     return rsp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)

