from passlib.context import CryptContext

# Setting up the Hashing Context for password hashing
# We tell it to use bcrypt algorithm for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a plain password (Create)
def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

# Function to verify a plain password against a hashed password (Authenticate) (Login)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
