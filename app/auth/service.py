from datetime import timedelta, datetime
from typing import Any, Dict, Optional, Union

from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth.schemas import CreateUser, UpdateUser, Token, TokenData, CreateUserCertification, UpdateUserCertification
from app.auth.models import User, UserCertification
from app.service.base import ServiceBase
from app import config

from passlib.context import CryptContext

from jose import JWTError, jwt
from pydantic import BaseModel

InvalidCredentialException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED, detail=[{"msg": "Could not validate credentials"}]
)

# Hash
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)


# oauth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)


# Token

# Generate Refresh Token Setting
def jwt_auth_init():
    # Generate Refresh Token Setting
    # in production you can use Settings management
    # from pydantic to get secret key from .env
    class Settings(BaseModel):
        authjwt_secret_key: str = config.JWT_SECRET

    # callback to get your configuration
    @AuthJWT.load_config
    def get_config():
        return Settings()
    # Generate Refresh Token Setting


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRES_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET, algorithm=config.JWT_ALG)

    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALG])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception


class ServiceUser(ServiceBase[User, CreateUser, UpdateUser]):
    def create(self, db: Session, *, obj_in: CreateUser) -> User:
        db_obj = User(
            username=obj_in.username,
            password=Hash.bcrypt(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            is_admin=obj_in.is_admin,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UpdateUser, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = Hash.bcrypt(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not Hash.verify(user.password, password):
            return None
        return user

    def change_password(self, db: Session, *, user: User, password: str) -> Optional[User]:
        user.password = Hash.bcrypt(password)
        db.commit()
        return True

    def login(self, user: User, db: Session):

        # generate refresh token
        Authorize = AuthJWT()
        access_token = Authorize.create_access_token(subject=user.username,
                                                     expires_time=timedelta(minutes=config.ACCESS_TOKEN_EXPIRES_TIME))

        return {"access_token": access_token, "token_type": "bearer"}

    def update_is_certification(self, db: Session, user: User, is_certification: bool = True) -> User:
        user.is_certification = is_certification
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_is_delete(self, db: Session, user: User, is_delete: bool = True):
        user.is_deleted = is_delete
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


class ServiceUserCertification(ServiceBase[UserCertification, CreateUserCertification, UpdateUserCertification]):
    def create_random_certification_number(self, db: Session, user: User):
        """
        해당 유저에 random certification number를 생성한다

        이미 존재하면 지우고 새로 만들어 준다
        """
        cert_exist = db.query(self.model).filter(UserCertification.user_id == user.id).first()
        if cert_exist:
            db.delete(cert_exist)
            db.commit()
        # Random number는 우선 임의로 지정한다 - 6글자 숫자로 지정
        from random import randrange
        result = self.create(db=db, obj_in=CreateUserCertification(
            user_id=user.id,
            certification_string='{0:06d}'.format(randrange(1, 1000000)),
        ))
        return result

    def confirm_certification_number(self, db: Session, user: User, cert_str: str,
                                     verified_time=datetime.now(),
                                     verified_duration=timedelta(minutes=5)
                                     ):
        """
        해당 user의 cert_str이 맞는지 True, False 반환
        인증 가능 시간을 지났는지도 검사
        :param verified_duration: TEST 값을 넣어줍니다. 인증 기간
        :param verified_time: TEST 값을 넣어줍니다. 인증 시간 기준
        :param db: Session
        :param user: 검색 하려는 유저
        :param cert_str: 검색하려는 certification string
        :return:
        """
        cert_by_user = db.query(self.model).filter(UserCertification.user_id == user.id).first()
        # 인증 시간 검사
        if cert_by_user.created_time > verified_time + verified_duration:
            return False

        # 문자열 검사
        if cert_by_user.certification_string == cert_str:
            return True
        else:
            return False


service_user = ServiceUser(User)
service_user_certification = ServiceUserCertification(UserCertification)
