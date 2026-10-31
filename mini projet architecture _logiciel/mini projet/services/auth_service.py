import sqlite3
from flask_bcrypt import generate_password_hash, check_password_hash

class AuthService:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def register(self, username, password, role="etudiant"):
        hashed = generate_password_hash(password).decode('utf-8')
        try:
            with self._conn() as conn:
                conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
            return True, "Utilisateur créé."
        except: 
            return False, "Erreur (Utilisateur déjà existant)."

    def login(self, username, password):
        with self._conn() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if user and check_password_hash(user['password'], password):
                return True, user
        return False, None

    def get_users(self):
        with self._conn() as conn:
            return [dict(row) for row in conn.execute("SELECT id, username, role FROM users").fetchall()]

    def delete_user(self, uid):
        try:
            with self._conn() as conn:
                user = conn.execute("SELECT id FROM users WHERE id = ?", (uid,)).fetchone()
                if not user:
                    return False, "Utilisateur introuvable."
                
                conn.execute("DELETE FROM users WHERE id = ?", (uid,))
                conn.commit()
            return True, "Utilisateur supprimé avec succès."
        except Exception as e:
            return False, str(e)

    def update_user(self, uid, data, is_gerant=False):
        try:
            with self._conn() as conn:
                # 1. Vérifier si l'utilisateur existe
                user = conn.execute("SELECT * FROM users WHERE id = ?", (uid,)).fetchone()
                if not user:
                    return False, "Utilisateur introuvable."

                # 2. Préparer les champs à modifier dynamiquement
                updates = []
                params = []

                # --- Champs modifiables par tout le monde (Propriétaire ou Gérant) ---
                if 'username' in data:
                    updates.append("username = ?")
                    params.append(data['username'])
                
                if 'password' in data:
                    hashed = generate_password_hash(data['password']).decode('utf-8')
                    updates.append("password = ?")
                    params.append(hashed)

                # --- Champs modifiables UNIQUEMENT par le gérant ---
                if is_gerant:
                    if 'role' in data:
                        updates.append("role = ?")
                        params.append(data['role'])
                    
                    if 'nom' in data:
                        updates.append("nom = ?")
                        params.append(data['nom'])
                    
                    if 'prenom' in data:
                        updates.append("prenom = ?")
                        params.append(data['prenom'])

                # 3. Vérification si des données valides ont été envoyées
                if not updates:
                    return False, "Aucune donnée valide à modifier."

                # 4. Construction et exécution de la requête SQL
                params.append(uid)
                query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
                
                conn.execute(query, params)
                conn.commit()
                
                return True, "Mise à jour réussie."

        except Exception as e:
            return False, str(e)
