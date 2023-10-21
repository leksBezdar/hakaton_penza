from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def check_record_existence(db: AsyncSession, model, record_id):
    record = await db.get(model, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"{model.__name__} was not found")
    return record
