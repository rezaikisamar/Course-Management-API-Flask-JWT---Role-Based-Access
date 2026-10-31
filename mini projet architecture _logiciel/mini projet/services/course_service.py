import sqlite3

class CourseService:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self._init_db()

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._conn() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, instructor TEXT, description TEXT)")

    def get_all(self):
        with self._conn() as conn:
            return [dict(row) for row in conn.execute("SELECT * FROM courses").fetchall()]

    def add(self, title, instructor, desc):
        with self._conn() as conn:
            cursor = conn.execute("INSERT INTO courses (title, instructor, description) VALUES (?, ?, ?)", (title, instructor, desc))
            conn.commit()
            return cursor.lastrowid

    def update(self, cid, title, instructor, desc):
        try:
            with self._conn() as conn:
                course = conn.execute("SELECT id FROM courses WHERE id = ?", (cid,)).fetchone()
                if not course: return False, "Cours introuvable."
                conn.execute("UPDATE courses SET title = ?, instructor = ?, description = ? WHERE id = ?", (title, instructor, desc, cid))
                conn.commit()
            return True, "Mis à jour avec succès."
        except Exception as e: return False, str(e)

    def delete(self, cid):
        try:
            with self._conn() as conn:
                course = conn.execute("SELECT id FROM courses WHERE id = ?", (cid,)).fetchone()
                if not course: return False, "Cours introuvable."
                conn.execute("DELETE FROM courses WHERE id = ?", (cid,))
                conn.commit()
            return True, "Supprimé avec succès."
        except Exception as e: return False, str(e)