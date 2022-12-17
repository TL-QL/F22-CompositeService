from flask import Flask, Response, request
from datetime import datetime
import json
from flask_cors import CORS

import requests

# Create the Flask application object.
app = Flask(__name__)

CORS(app)

user_base_url = 'http://6156usermicroserviceversion1-env.eba-hzmwy7da.us-east-1.elasticbeanstalk.com'
contacts_base_url = 'http://35.172.211.153:5011'


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


@app.route("/api/composite/email/<email>", methods=["GET"])
def get_composite_by_email(email):

    user_url = user_base_url + "/api/users/email/"+ email
    response = requests.get(user_url)

    if response.status_code != 200:
        rsp = Response("user NOT FOUND", status=404, content_type="text/plain")
        return rsp

    user = response.json()

    contacts_url = contacts_base_url + "/api/contacts/id/"+user.get("email")
    response = requests.get(contacts_url)

    if response.status_code != 200:
        rsp = Response("contacts NOT FOUND", status=response.status_code, content_type="text/plain")
        return rsp

    contact = response.json()

    result = {
        "uid": user.get("uid"),
        "last_name": user.get("last_name"),
        "first_name": user.get("first_name"),
        "middle_name": user.get("middle_name"),
        "username": user.get("username"),
        "contacts": contact
    }

    rsp = Response(json.dumps(result), status=200, content_type="application.json")

    return rsp


@app.route("/api/composite/create/<email>/<lname>/<fname>/<mname>/<username>", methods=["POST"])
def create_contacts_by_email(email, lname, fname, mname, username):

    args = request.args
    contacts = args.getlist('contact')

    user_url = user_base_url + "/api/users/update/"+email+"/"+lname+"/"+fname+"/"+mname+"/"+username
    response = requests.post(user_url)

    if response.status_code != 200:
        print(response)
        rsp = Response("user failed", status=response.status_code, content_type="text/plain")
        return rsp
    
    contact_url = contacts_base_url + "/api/contacts/create/"+email
    if len(contacts) == 0:
        url = contact_url+"/"+"email"+"/"+email+"/"+"personal"
        response = requests.post(url)
        if response.status_code != 200:
            msg = "Add default email failed"
            rsp = Response(msg, status=response.status_code, content_type="text/plain")
            return rsp
    for contact in contacts:
        contact = json.loads(contact)
        url = contact_url+"/"+contact.get("type")+"/"+contact.get("contact")+"/"+contact.get("kind")
        response = requests.post(url)
        if response.status_code != 200:
            msg = contact.get("type") +" "+contact.get("kind")+ " failed"
            rsp = Response(msg, status=response.status_code, content_type="text/plain")
            return rsp

    rsp = Response("success", status=200, content_type="application.json")

    return rsp

@app.route("/api/composite/delete/<email>", methods=["POST"])
def delete_composite_by_email(email):

    # delete user
    user_url = user_base_url + "/api/users/email/"+ email
    response = requests.get(user_url)

    if response.status_code != 200:
        rsp = Response("USER NOT FOUND", status=404, content_type="text/plain")
        return rsp

    user_url = user_base_url + "/api/users/delete/"+email
    response = requests.post(user_url)
    if response.status_code != 200:
        print(response)
        rsp = Response("delete user failed", status=response.status_code, content_type="text/plain")
        return rsp

    # delete contact
    contacts_url = contacts_base_url + "/api/contacts/id/"+email
    response = requests.get(contacts_url)
    if response.status_code != 200:
        rsp = Response("SUCCESS -- NO CONTACT FOR USER", status=200, content_type="text/plain")
        return rsp

    contacts = response.json()

    for con in contacts:
        t = con.get("type")
        k = con.get("kind")
        url = contacts_base_url + "/api/contacts/delete/" + email + "/" + t + "/" + k
        response = requests.delete(url)

        if response.status_code != 200:
            msg = "delete " + t + " and " + k + " failed"
            rsp = Response(msg, status=response.status_code, content_type="text/plain")
            return rsp


    rsp = Response("success", status=200, content_type="application.json")
    return rsp


@app.route("/api/composite/update/<email>/<lname>/<fname>/<mname>/<username>", methods=["POST"])
def update_contacts_by_email(email, lname, fname, mname, username):

    user_url = user_base_url + "/api/users/update/"+email+"/"+lname+"/"+fname+"/"+mname+"/"+username
    response = requests.post(user_url)

    if response.status_code != 200:
        print(response)
        rsp = Response("update user failed", status=response.status_code, content_type="text/plain")
        return rsp
    
    args = request.args
    input_contact = args.getlist('contact')

    # delete contact
    delete_url = contacts_base_url + "/api/contacts/id/"+email
    response = requests.get(delete_url)
    
    if response.status_code == 200:
        contacts = response.json()
        for con in contacts:
            t = con.get("type")
            k = con.get("kind")
            url = contacts_base_url + "/api/contacts/delete/" + email + "/" + t + "/" + k
            print(url)
            response = requests.delete(url)

            if response.status_code != 200:
                msg = "delete " + t + " and " + k + " failed"
                rsp = Response(msg, status=response.status_code, content_type="text/plain")
                return rsp

    contact_url = contacts_base_url + "/api/contacts/create/"+email
    for contact in input_contact:
        contact = json.loads(contact)
        url = contact_url+"/"+contact.get("type")+"/"+contact.get("contact")+"/"+contact.get("kind")
        response = requests.post(url)
        if response.status_code != 200:
            msg = contact.get("type") +" "+contact.get("kind")+ " failed"
            rsp = Response(msg, status=response.status_code, content_type="text/plain")
            return rsp

    rsp = Response("success", status=200, content_type="application.json")
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

