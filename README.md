# lab-py-rbac-system
RBAC System

Create virtual environment:
python -m venv venv
source venv/bin/activate   # Mac/Linux

Install packages:
pip install fastapi uvicorn sqlalchemy passlib[argon2] python-jose python-multipart pydantic[email] python-dotenv

Run the Server:
uvicorn app.main:app --reload

http://127.0.0.1:8000/docs
