from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature.models import Temperature
from temperature.schemas import TemperatureRequest


async def get_temperature(db: AsyncSession, city_id: str | None = None):
    query = select(Temperature).options(selectinload(Temperature.city))

    if city_id:
        query = query.where(Temperature.city_id == city_id)

    result = await db.execute(query)

    return result.scalars().all()


def build_temperature(data: TemperatureRequest) -> Temperature:
    return Temperature(**data.model_dump())


async def create_temperature(db: AsyncSession, data: TemperatureRequest):
    temperature = build_temperature(data)
    db.add(temperature)
    await db.commit()
    await db.refresh(temperature)
    return temperature


async def create_temperatures(
    db: AsyncSession, data_list: List[TemperatureRequest]
):
    temperatures = [build_temperature(data) for data in data_list]
    db.add_all(temperatures)
    await db.commit()
    for temp in temperatures:
        await db.refresh(temp)
    return temperatures
