from fastapi import APIRouter, Depends, HTTPException, status

from app.activity.schema import ActivityRead, ActivitySetMaxLevel
from app.activity.service import ActivityService, get_activity_service
from core.auth import api_key_auth
from core.base.schema import ResponseSchema

router = APIRouter(
    prefix="/api/v1/activity",
    tags=["activity"],
    dependencies=[Depends(api_key_auth)],
)


@router.post("/set-max-level", response_model=ResponseSchema[ActivityRead])
async def set_activity_max_level(
    data: ActivitySetMaxLevel,
    activity_service: ActivityService = Depends(get_activity_service),
):
    """Установить ограничение уровня вложенности для деятельности."""
    result = await activity_service.set_max_level_by_name(data.name, data.max_level)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Деятельность '{data.name}' не найдена",
        )
    return ResponseSchema(data=result)
