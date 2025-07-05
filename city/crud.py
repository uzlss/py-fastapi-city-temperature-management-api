from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from city.schemas import CityRequest


async def get_cities(db: AsyncSession):
    query = select(City)
    result = await db.execute(query)
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, id: int):
    query = select(City).where(City.id == id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_city(db: AsyncSession, data: CityRequest):
    query = insert(City).values(**data.model_dump()).returning(City)
    result = await db.execute(query)
    await db.commit()
    return result.scalar_one()


async def delete_city(db: AsyncSession, id: int):
    city = await get_city_by_id(db, id)
    if not city:
        return None

    query = delete(City).where(City.id == city.id)
    await db.execute(query)
    await db.commit()
    return city
