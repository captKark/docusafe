from datetime import datetime, timedelta, timezone
from jose import jwt
# 1. SECRET KEY: The secret used to sign the JWT tokens
# If the hacker gets this, they can forge the keys, so keep it safe!
SECRET_KEY = "super_secret_key_for_dev_only"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
def create_access_token(data: dict):
    to_encode = data.copy()

    # Set the expiration time for the token (current time + 60 mins)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add the expiration time to the payload
    to_encode.update({"exp": expire})

    # encode the JWT token with the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
