from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import models, database, auth, dependencies

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/register")
def register(user_data: dependencies.UserCreate, db: Session = Depends(dependencies.get_db)):
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
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(permission: bool = Depends(dependencies.permission_required("read_data"))):
    return {"message": "You have access to this protected route"}
