from fastapi import Depends , HTTPException , status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv

API_KEY_NAME = "api-key"

api_key_header = APIKeyHeader(name = API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    allowed_api_keys = os.getenv("API_KEYS",allowed_api_keys)

    if api_key not in allowed_api_keys:
        print("api key is invalid.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    print("api key is valid.")
    return api_key