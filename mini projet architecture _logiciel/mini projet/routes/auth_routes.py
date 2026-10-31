from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from auth.auth_handler import encode_token, decode_token

auth_bp = Blueprint('auth', __name__)
s = AuthService()

@auth_bp.route('/register', methods=['POST'])
def reg():
    data = request.json
    if not data: return jsonify({"err": "JSON manquant"}), 400
    
    success, msg = s.register(data['username'], data['password'], data.get('role', 'etudiant'))
    return jsonify({"msg": msg}), 201 if success else 400

@auth_bp.route('/login', methods=['POST'])
def log():
    data = request.json
    if not data: return jsonify({"err": "JSON manquant"}), 400
    
    success, user = s.login(data['username'], data['password'])
    if success:
        token = encode_token(user['id'], user['role'])
        return jsonify({"token": token, "role": user['role']}), 200
    return jsonify({"err": "Infos incorrectes"}), 401

@auth_bp.route('/users', methods=['GET'])
def list_u():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"err": "Header Authorization manquant"}), 401

    try:
        # On sépare "Bearer" du "token"
        parts = auth_header.split(" ")
        if len(parts) != 2:
            return jsonify({"err": "Format invalide. Utilisez: Bearer <token>"}), 401

        token = parts[1]
        pay = decode_token(token)

        if pay is None:
            return jsonify({"err": "Token invalide (clé différente ou expiré)"}), 401

        # Vérification du rôle (on force en minuscules pour éviter les erreurs)
        user_role = str(pay.get('role', '')).lower()
        if user_role != 'gerant':
            return jsonify({"err": f"Accès refusé. Ton rôle est: {user_role}"}), 403

        return jsonify(s.get_users()), 200

    except Exception as e:
        return jsonify({"err": f"Erreur interne : {str(e)}"}), 500
@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_u(user_id):
    # 1. Récupération du header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"err": "Header Authorization manquant"}), 401

    try:
        # 2. Extraction et décodage du token
        parts = auth_header.split(" ")
        if len(parts) != 2:
            return jsonify({"err": "Format invalide"}), 401

        token = parts[1]
        pay = decode_token(token)

        if pay is None:
            return jsonify({"err": "Token invalide"}), 401

        # 3. Vérification du rôle gérant (sécurité)
        if str(pay.get('role', '')).lower() != 'gerant':
            return jsonify({"err": "Accès interdit : seul le gérant peut supprimer"}), 403

        # 4. Exécution de la suppression via le service
        success, msg = s.delete_user(user_id)
        
        if success:
            return jsonify({"msg": msg}), 200
        else:
            return jsonify({"err": msg}), 404

    except Exception as e:
        return jsonify({"err": f"Erreur interne : {str(e)}"}), 500
@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_u(user_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"err": "Token manquant"}), 401

    token = auth_header.split(" ")[1]
    pay = decode_token(token)
    if pay is None:
        return jsonify({"err": "Token invalide"}), 401

    current_user_id = int(pay.get('sub'))
    current_role = str(pay.get('role', '')).lower()
    data = request.json

    # LOGIQUE DE SÉCURITÉ
    is_gerant = (current_role == 'gerant')
    is_own_account = (current_user_id == user_id)

    if is_gerant:
        # Le gérant peut tout modifier
        success, msg = s.update_user(user_id, data, is_gerant=True)
    elif is_own_account:
        # L'étudiant modifie son propre compte (nom et password seulement)
        # On filtre les données pour empêcher l'étudiant de changer son rôle lui-même
        allowed_data = {k: v for k, v in data.items() if k in ['username', 'password']}
        success, msg = s.update_user(user_id, allowed_data, is_gerant=False)
    else:
        # Un étudiant essaie de modifier le compte d'un autre
        return jsonify({"err": "Action interdite"}), 403

    if success:
        return jsonify({"msg": msg}), 200
    return jsonify({"err": msg}), 400