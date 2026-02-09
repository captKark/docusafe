from slowapi import Limiter
from slowapi.util import get_remote_address # <-- Import the function to get client's IP address

# Initialize the Limiter with the function to get client's IP address
limiter = Limiter(key_func=get_remote_address)
# key_func=get_remote_address means 'get the client's IP address to use as the key for rate limiting'
