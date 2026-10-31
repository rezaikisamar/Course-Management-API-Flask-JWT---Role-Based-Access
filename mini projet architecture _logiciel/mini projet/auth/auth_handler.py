import jwt
import datetime

# Une clé longue pour éviter les erreurs de sécurité
SECRET_KEY = "Ceci_Est_Une_Cle_Tres_Longue_Pour_Le_Projet_M1_De_Samar_2026"

def encode_token(user_id, role):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': str(user_id),  # <--- AJOUTE str() ICI
        'role': role
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception as e:
        print(f"ERREUR DECODAGE : {e}")
        return None