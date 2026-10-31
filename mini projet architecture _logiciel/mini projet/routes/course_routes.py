from flask import Blueprint, request, jsonify
from services.course_service import CourseService
from auth.auth_handler import decode_token

course_bp = Blueprint('courses', __name__)
s = CourseService()

# GET http://127.0.0.1:5000/courses
@course_bp.route('/', methods=['GET'])
def get_c():
    return jsonify(s.get_all()), 200

# POST http://127.0.0.1:5000/courses
@course_bp.route('/', methods=['POST'])
def add_c():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"err": "Token manquant"}), 401
    
    token = auth_header.split(" ")[1]
    pay = decode_token(token)
    
    if not pay or pay.get('role') not in ['gerant', 'enseignant']:
        return jsonify({"err": "Action réservée au staff"}), 403
    
    data = request.json
    if not data:
        return jsonify({"err": "Données JSON manquantes"}), 400
        
    nid = s.add(data['title'], data['instructor'], data.get('description', ''))
    return jsonify({"id": nid}), 201

# PUT http://127.0.0.1:5000/courses/1
@course_bp.route('/<int:cid>', methods=['PUT'])
def update_c(cid):
    auth_header = request.headers.get("Authorization")
    if not auth_header: return jsonify({"err": "Token manquant"}), 401
    
    token = auth_header.split(" ")[1]
    pay = decode_token(token)
    
    if not pay or pay.get('role') not in ['gerant', 'enseignant']:
        return jsonify({"err": "Accès interdit"}), 403
    
    data = request.json
    success, msg = s.update(cid, data['title'], data['instructor'], data.get('description', ''))
    return jsonify({"msg" if success else "err": msg}), 200 if success else 404

# DELETE http://127.0.0.1:5000/courses/1
@course_bp.route('/<int:cid>', methods=['DELETE'])
def delete_c(cid):
    auth_header = request.headers.get("Authorization")
    if not auth_header: return jsonify({"err": "Token manquant"}), 401
    
    token = auth_header.split(" ")[1]
    pay = decode_token(token)
    
    if not pay or pay.get('role') not in ['gerant', 'enseignant']:
        return jsonify({"err": "Accès interdit"}), 403
    
    success, msg = s.delete(cid)
    return jsonify({"msg" if success else "err": msg}), 200 if success else 404