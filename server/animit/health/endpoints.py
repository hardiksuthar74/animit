from fastapi import APIRouter


router = APIRouter(tags=["health"], include_in_schema=False)


@router.get("/healthz")
async def healthz():
    return {"status": "ok"}
