import os
from dotenv import load_dotenv
import bcrypt
from datetime import datetime, timedelta, UTC
from jose import jwt

# Carrega o .env da pasta backend
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Configurações para JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, db_session=None, ip_address: str = None):
    """
    Verify JWT token and optionally log security events.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            if db_session:
                from .logging_utils import log_security_event, GameAction
                log_security_event(
                    db=db_session,
                    action=GameAction.LOGIN,
                    ip_address=ip_address,
                    details={
                        "token_verification": "failed",
                        "reason": "Missing email or user_id in token",
                        "success": False
                    }
                )
            return None
            
        # Token is valid, could log successful verification if needed
        # for high-security applications
        return {"email": email, "user_id": user_id}
        
    except jwt.ExpiredSignatureError:
        if db_session:
            from .logging_utils import log_security_event, GameAction
            log_security_event(
                db=db_session,
                action=GameAction.LOGIN,
                ip_address=ip_address,
                details={
                    "token_verification": "failed",
                    "reason": "Token expired",
                    "success": False
                }
            )
    except jwt.JWTError:
        if db_session:
            from backend.app.utils.logging_utils import log_security_event, GameAction
            log_security_event(
                db=db_session,
                action=GameAction.LOGIN,
                ip_address=ip_address,
                details={
                    "token_verification": "failed",
                    "reason": "Invalid token",
                    "success": False
                }
            )
    except Exception as e:
        if db_session:
            from backend.app.utils.logging_utils import log_error, GameAction
            log_error(
                db=db_session,
                action=GameAction.LOGIN,
                error_message=f"Token verification error: {str(e)}",
                details={
                    "token_verification": "error",
                    "exception_type": type(e).__name__
                }
            )
    return None
