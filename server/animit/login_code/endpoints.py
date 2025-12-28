from fastapi import APIRouter, Depends, HTTPException, Request

from animit.login_code.schemas import AuthenticateRequest, LoginCodeRequest
from animit.kit.db.postgres import AsyncSession
from animit.postgres import get_db_session

from animit.login_code.service import (
    LoginCodeInvalidOrExpired,
    login_code as login_code_service,
)

router = APIRouter(prefix="/login-code", tags=["login_code"])


@router.post("/request")
async def login(
    login_code_request: LoginCodeRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Request a login code
    """

    code_model, code = await login_code_service.request(
        session,
        login_code_request.email,
    )

    # Send the code email
    await login_code_service.send(code_model, code)


@router.post("/authenticate")
async def authenticate(
    request: Request,
    authenticate_request: AuthenticateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Authenticate with a login code.
    """
    try:
        user, is_signup = await login_code_service.authenticate(
            session,
            code=authenticate_request.code,
            email=authenticate_request.email,
        )
    except LoginCodeInvalidOrExpired as e:
        raise HTTPException(detail=str(e), status_code=e.status_code)
