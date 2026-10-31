def validate_user(data):
    if not data or "username" not in data or "password" not in data:
        return False, "Champs obligatoires manquants."
    return True, None

def validate_course(data):
    if not data or "title" not in data:
        return False, "Le titre du cours est obligatoire."
    return True, None