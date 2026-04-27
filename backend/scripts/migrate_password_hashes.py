"""Idempotent password migration script: plaintext -> secure hash."""
from app import create_app
from app.models import db
from app.models.usuario import Usuario
from app.security import hash_password, is_password_hashed


def migrate_passwords() -> tuple[int, int]:
    total = 0
    updated = 0

    users = Usuario.query.all()
    for user in users:
        total += 1
        if not user.clave:
            continue
        if is_password_hashed(user.clave):
            continue

        user.clave = hash_password(user.clave)
        updated += 1

    if updated:
        db.session.commit()

    return total, updated


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        total_users, updated_users = migrate_passwords()
        print(f"Usuarios revisados: {total_users}")
        print(f"Claves migradas: {updated_users}")
