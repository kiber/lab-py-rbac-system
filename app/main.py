from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import auth, crud, database, dependencies, models, schemas, seed_database
from .errors import raise_api_error, register_exception_handlers

models.Base.metadata.create_all(bind=database.engine)
seed_database.seed()

app = FastAPI()
register_exception_handlers(app)

@app.post("/register")
def register(user_data: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    existing_user = db.query(models.User).filter(
        models.User.username == user_data.username
    ).first()
    existing_email = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()

    if existing_user:
        raise_api_error(
            status_code=status.HTTP_409_CONFLICT,
            code="username_exists",
            message="Username already registered",
        )
    if existing_email:
        raise_api_error(
            status_code=status.HTTP_409_CONFLICT,
            code="email_exists",
            message="Email already registered",
        )

    hashed = auth.hash_password(user_data.password)
    user = models.User(
        username=user_data.username,
        email=user_data.email,
        password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        raise_api_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_credentials",
            message="Invalid credentials",
        )

    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(permission: bool = Depends(dependencies.has_permission("read_data"))):
    return {"message": "You have access to this protected route"}

# Start - Permission Endpoints
@app.post("/permissions/", response_model=schemas.PermissionResponse)
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_permission(db, permission.name)

@app.get("/permissions/", response_model=list[schemas.PermissionResponse])
def list_permissions(db: Session = Depends(dependencies.get_db)):
    return crud.get_permissions(db)

@app.delete("/permissions/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(dependencies.get_db)):
    crud.delete_permission(db, permission_id)
    return {"message": "Permission deleted"}
# End - Permission Endpoints

# Start - Role Endpoints
@app.post("/roles/", response_model=schemas.RoleResponse)
def create_role(role: schemas.RoleCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_role(db, role.name)

@app.get("/roles/", response_model=list[schemas.RoleResponse])
def list_roles(db: Session = Depends(dependencies.get_db)):
    return crud.get_roles(db)

@app.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(dependencies.get_db)):
    crud.delete_role(db, role_id)
    return {"message": "Role deleted"}

@app.put("/roles/{role_id}/permissions")
def assign_permissions(role_id: int, data: schemas.AssignPermission, db: Session = Depends(dependencies.get_db)):
    return crud.assign_permissions_to_role(db, role_id, data.permission_ids)
# End - Role Endpoints

# Start - Assign Role to User
@app.put("/users/{user_id}/roles")
def assign_roles(user_id: int, data: schemas.AssignRole, db: Session = Depends(dependencies.get_db)):
    return crud.assign_roles_to_user(db, user_id, data.role_ids)
# End - Assign Role to User
