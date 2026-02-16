from . import models, database

def seed():
    db = database.SessionLocal()

    # Create default permissions
    default_permissions = ["read_data", "write_data", "delete_data"]

    for perm_name in default_permissions:
        existing = db.query(models.Permission).filter_by(name=perm_name).first()
        if not existing:
            db.add(models.Permission(name=perm_name))
    db.commit()

    # Create Admin role
    admin_role = db.query(models.Role).filter_by(name="Admin").first()
    if not admin_role:
        admin_role = models.Role(name="Admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    # Assign all permissions to Admin
    permissions = db.query(models.Permission).all()
    admin_role.permissions = permissions
    db.commit()
    db.close()
