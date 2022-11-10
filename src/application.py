from flask import Flask, Response, request
from datetime import datetime
import json
from contact_resource import ContactResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


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


@app.route("/api/contacts/id/<uid>", methods=["GET"])
def get_contacts_by_uid(uid):

    result = ContactResource.get_by_key(uid)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/contacts/query/<queryString>/<offset>/<limit>", methods=["GET"])
def get_contacts_by_query(queryString, offset, limit):

    result = ContactResource.get_by_query(queryString, int(offset), int(limit))

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/contacts/create/<uid>/<type>/<contact>/<kind>", methods=["POST"])
def create_contacts_by_uid(uid, type, contact, kind):

    result = ContactResource.create_by_key(uid, type, contact, kind)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/contacts/update/<uid>/<type>/<contact>/<kind>", methods=["PUT"])
def update_contacts_by_uid(uid, type, contact, kind):

    result = ContactResource.update_by_key(uid, type, contact, kind)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/contacts/delete/<uid>/<type>/<kind>", methods=["DELETE"])
def delete_contacts_by_uid(uid, type, kind):

    result = ContactResource.delete_by_key(uid, type, kind)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)

