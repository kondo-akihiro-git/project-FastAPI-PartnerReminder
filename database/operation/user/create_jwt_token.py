import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
# JWTのシークレットとアルゴリズム（環境変数にした方が良い）
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXP_DELTA_SECONDS = os.getenv("JWT_EXP_DELTA_SECONDS")

def create_jwt_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=int(JWT_EXP_DELTA_SECONDS))
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token