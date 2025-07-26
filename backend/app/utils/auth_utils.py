
import bcrypt
from datetime import datetime, timedelta, UTC
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.config import JWT_SECRET_KEY

# OAuth2 scheme for FastAPI authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

# JWT configuration variables
SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password using bcrypt.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token with an optional expiration delta.
    """
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
    Verify a JWT token and optionally log security events.
    Returns a dict with user info if valid, otherwise None.
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
    except jwt.JWTError as e:
        if db_session:
            from backend.app.utils.logging_utils import log_security_event, GameAction
            log_security_event(
                db=db_session,
                action=GameAction.LOGIN,
                ip_address=ip_address,
                details={
                    "token_verification": "failed",
                    "reason": f"Invalid token: {str(e)}",
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

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    FastAPI dependency to get the current authenticated user from the JWT token.
    Raises HTTPException if credentials are invalid.
    Returns the full User object from the database.
    """
    from database.models import User
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_data = verify_token(token, db_session=db)
    if not user_data or not user_data.get("user_id"):
        raise credentials_exception
    
    # Get the full user object from database
    user_id = user_data["user_id"]
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise credentials_exception
        
    return user
