from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.organization.crud import organization
from app.organization.schema import GeoBoundsQuery, GeoRadiusQuery, OrganizationRead
from app.organization.service import OrganizationService, get_organization_service
from core.auth import api_key_auth
from core.base.schema import ResponseListSchema, ResponseSchema
from core.database.session import get_async_session

router = APIRouter(
    prefix="/api/v1/organization",
    tags=["organization"],
    dependencies=[Depends(api_key_auth)],
)


@router.get("/{organization_id}", response_model=ResponseSchema[OrganizationRead])
async def get_organization(
    organization_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить организацию по её идентификатору.

    Args:
        organization_id: Уникальный идентификатор организации.
        session: Асинхронная сессия базы данных.

    Returns:
        ResponseSchema[OrganizationRead]: Данные организации.

    Raises:
        HTTPException: 404 если организация не найдена.
    """
    organization_obj = await organization.get_by_id(session, organization_id)
    if organization_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
        )
    return ResponseSchema(data=OrganizationRead.model_validate(organization_obj))


@router.get(
    "/building/{building_address}", response_model=ResponseListSchema[OrganizationRead]
)
async def get_organizations_by_building_address(
    building_address: str,
    organization_service: OrganizationService = Depends(get_organization_service),
):
    """
    Получить список организаций по адресу здания.

    Args:
        building_address: Адрес здания для поиска организаций.
        organization_service: Сервис для работы с организациями.

    Returns:
        ResponseListSchema[OrganizationRead]: Список организаций в указанном здании.

    Raises:
        HTTPException: 500 при ошибке сервера.
    """
    try:
        organizations = (
            await organization_service.get_organizations_by_building_address(
                building_address
            )
        )
        return ResponseListSchema(data=organizations)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/activity/{activity_name}", response_model=ResponseListSchema[OrganizationRead]
)
async def get_organizations_by_activity(
    activity_name: str,
    organization_service: OrganizationService = Depends(get_organization_service),
):
    """
    Получить список организаций по названию вида деятельности.

    Args:
        activity_name: Название вида деятельности.
        organization_service: Сервис для работы с организациями.

    Returns:
        ResponseListSchema[OrganizationRead]: Список организаций с указанным видом деятельности.

    Raises:
        HTTPException: 500 при ошибке сервера.
    """
    try:
        organizations = await organization_service.get_organizations_by_activity_name(
            activity_name
        )
        return ResponseListSchema(data=organizations)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/name/{name}", response_model=ResponseSchema[OrganizationRead])
async def get_organization_by_name(
    name: str,
    organization_service: OrganizationService = Depends(get_organization_service),
):
    """
    Получить организацию по её названию.

    Args:
        name: Название организации для поиска.
        organization_service: Сервис для работы с организациями.

    Returns:
        ResponseSchema[OrganizationRead]: Данные найденной организации.

    Raises:
        HTTPException: 404 если организация не найдена, 500 при ошибке сервера.
    """
    try:
        organization_obj = await organization_service.get_organization_by_name(name)
        if organization_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found"
            )
        return ResponseSchema(data=organization_obj)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/activity-tree/{activity_name}",
    response_model=ResponseListSchema[OrganizationRead],
)
async def get_organizations_by_activity_tree(
    activity_name: str,
    organization_service: OrganizationService = Depends(get_organization_service),
):
    """
    Получить организации по виду деятельности и всем дочерним видам.
    Например: "Еда" → организации с Еда, Мясная продукция, Молочная продукция.
    """
    try:
        organizations = (
            await organization_service.get_organizations_by_activity_with_children(
                activity_name
            )
        )
        return ResponseListSchema(data=organizations)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/geo/radius", response_model=ResponseListSchema[OrganizationRead])
async def get_organizations_in_radius(
    query: GeoRadiusQuery = Depends(),
    organization_service: OrganizationService = Depends(get_organization_service),
):
    """Получить организации в радиусе от точки."""
    try:
        organizations = await organization_service.get_organizations_in_radius(
            query.lat, query.lon, query.radius_km
        )
        return ResponseListSchema(data=organizations)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/geo/bounds", response_model=ResponseListSchema[OrganizationRead])
async def get_organizations_in_bounds(
    query: GeoBoundsQuery = Depends(),
    organization_service: OrganizationService = Depends(get_organization_service),
):
    """Получить организации в прямоугольной области."""
    try:
        organizations = await organization_service.get_organizations_in_bounds(
            query.min_lat, query.min_lon, query.max_lat, query.max_lon
        )
        return ResponseListSchema(data=organizations)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
