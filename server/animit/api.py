from fastapi import APIRouter
from animit.login_code.endpoints import router as login_code_router

router = APIRouter(prefix="/v1")


router.include_router(login_code_router)
