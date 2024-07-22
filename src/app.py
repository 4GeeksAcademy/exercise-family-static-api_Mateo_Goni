import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_new_member():
    request_body = request.json
    if not request_body or not isinstance(request_body, dict):
        return jsonify({"error": "Bad request, invalid JSON"}), 400
    
    required_fields = ["first_name", "age", "lucky_numbers"]
    if not all(field in request_body for field in required_fields):
        return jsonify({"error": "Bad request, missing fields"}), 400
    
    try:
        jackson_family.add_member(request_body)
        return jsonify({"msg": "Member added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        jackson_family.delete_member(id)
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    request_body = request.json
    if not request_body or not isinstance(request_body, dict):
        return jsonify({"error": "Bad request, invalid JSON"}), 400
    
    request_body["id"] = id
    if not jackson_family.update_member(request_body):
        return jsonify({"error": "Member not found"}), 404
    
    return jsonify({"msg": "Member updated successfully"}), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
