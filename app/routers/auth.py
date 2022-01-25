from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_jwt_auth.exceptions import JWTDecodeError
from fastapi_mail import FastMail
from sqlalchemy.orm import Session

from fastapi_jwt_auth import AuthJWT
from starlette.background import BackgroundTasks
from starlette.responses import Response

from app.auth.schemas import RequestUserCertification, ConfirmUserCertification
from app.database.core import get_db

from app.auth import schemas as auth_schemas
from app.email.core import get_fm
from app.email.schemas import SendEmail
from app.email.service import service_email
from app.log.schemas import CreateLog
from app.log.service import service_log

from app.routers.util import get_summary_location
from app.auth.service import service_user, service_user_certification

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=auth_schemas.ShowUser, responses={
    409: {
        "description": "Error: Conflict",
    },
},
             summary=get_summary_location())
def create(request: auth_schemas.CreateUser, db: Session = Depends(get_db)):
    """
    ### 설명
    - User 생성
    ### Request Body
    - username : User 의 아이디
    - password : User 의 패스워드
    - first_name : User 의 first name
    - last_name : User 의 last name
    - is_admin : User 의 admin 여부(true, false 둘 중 하나)
    ### 관련 모델
    - User
    """
    user = service_user.get_by_username(db=db, username=request.username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Username {request.username} is already used')

    # model id 가 각 model명_id로 변경되어 해당 log 함수는 사용이 불가능 합니다 - log 생성 함수 새로 만들어야함
    # create_log(actor_id=1, action='CREATE', element=new_user, db=db)

    new_user = service_user.create(db, obj_in=request)
    service_log.create(db_obj=new_user, actor_name=new_user.username, action="CREATE")
    return new_user


@router.get('/identifier', status_code=status.HTTP_200_OK, response_model=auth_schemas.ShowUser, responses={
    404: {
        "description": "Error: Not Found",
    },
}, summary=get_summary_location())
def check_id(username: str, db: Session = Depends(get_db)):
    """
    ### 설명
    - username 있는지 확인
    - username 는 email(아이디)을 의미함
    ### 파라미터
    - username : User 의 아이디
    ### 관련 모델
    - User
    """
    user = service_user.get_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.post('/login', status_code=status.HTTP_200_OK, responses={
    404: {
        "description": "Error: Not Found",
    },
}, summary=get_summary_location())
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    ### 설명
    - login 확인 후 token 반환
    ### Request Body
    - username : User 의 아이디
    - password : User 의 패스워드
    - 기타 로그인 관련 파라미터들
    ### 관련 모델
    - User
    """
    user = service_user.get_by_username(db, username=request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')

    if not service_user.authenticate(db, username=request.username, password=request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Incorrect password')

    logined_user = service_user.login(db=db, user=user)
    service_log.create(db_obj=user, actor_name=user.username, action="CREATE")
    return logined_user


@router.put('/password', status_code=status.HTTP_200_OK, responses={
    404: {
        "description": "Error: Not Found",
    },
}, summary=get_summary_location())
def change_password(request: auth_schemas.ChangePassword, db: Session = Depends(get_db)):
    """
    ### 설명
    - password 변경
    ### Request Body
    - username : User 의 아이디
    - new_password : 새로운 패스워드
    - check_password: 새로운 패스워드 확인
    ### 관련 모델
    - User
    """
    user = service_user.get_by_username(db, username=request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {request.username} is not available')
    if request.new_password != request.check_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Password does not matched')

    if not service_user.change_password(db=db, user=user, password=request.new_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'change Password Error')

    service_log.create(db_obj=user, actor_name=user.username, action="UPDATE")

    return "done"


@router.put('/password/init', status_code=status.HTTP_200_OK, summary=get_summary_location())
def init_pw():
    """
    ### 설명
    - password 초기화
    - 아직 구현 안됨
    ### 관련 모델
    - User
    """
    pass


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, responses={
    404: {
        "description": "Error: Not Found",
    },
}, summary=get_summary_location())
def delete(user_id: int, db: Session = Depends(get_db)):
    """
    ### 설명
    - User 삭제
    ### 파라미터
    - user_id : User 의 ID(username 이 아닌 user_id 을 의미)
    ### 관련 모델
    - User
    """
    user = service_user.get_by_user_id(id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
    service_user.remove(db, id)

    service_log.create(db_obj=user, actor_name=user.username, action="DELETE")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authauth/login")


@router.post('/certification/request',
             status_code=status.HTTP_201_CREATED,
             summary=get_summary_location())
async def request_certification_number(request: RequestUserCertification,
                                       fm: FastMail = Depends(get_fm),
                                       db: Session = Depends(get_db)):
    """
    ### 설명
    - 해당 user을 인증하기 위한 번호흫 username에 전송

    ### request body
    - username : 인증 번호를 보낼 email(username)
    """
    user = service_user.get_by_username(db=db, username=request.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User Username {request.username} does not exist')

    cert_str = service_user_certification.create_random_certification_number(db=db, user=user)
    # 이메일 전송
    with fm.record_messages() as outbox:
        send_email = SendEmail(
            receiver=user.username,
            title='Certification',
            content=cert_str.certification_string,
        )
        await service_email.send_certification_user_link_email_async(fm=fm,
                                                                     email_to_list=[user.username],
                                                                     subject='인증 번호 전달',
                                                                     body=send_email)
    return {'created_time': cert_str.created_time}


@router.post('/certification/confirm',
             status_code=status.HTTP_200_OK,
             response_model=bool,
             summary=get_summary_location())
def confirm_certification_number(request: ConfirmUserCertification, db: Session = Depends(get_db)):
    """
    ### 설명
    - User id의 profile 정보 반환

    profile이 없는 경우 None이 반환됩니다
    ### 관련 모델
    - user_id : 찾으려는 auth id
    """
    user = service_user.get_by_username(db=db, username=request.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User Username {request.username} does not exist')

    confirm_result = service_user_certification.confirm_certification_number(db=db, user=user,
                                                                             cert_str=request.certification_string)

    if confirm_result:  # 승인 절차 시행  user를 승인으로 바꾸고 true return
        service_user.update_is_certification(db=db, user=user)
        service_user_certification.remove(db=db, id=user.user_certification.id)
        return True
    else:  # 문자 안맞음 다시 보내야함
        return False
