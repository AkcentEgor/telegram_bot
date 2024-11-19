from models_db import MeterReading, async_session
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.future import select


app = FastAPI()

class MoveMeter(BaseModel):
    personal_account: int
    meter: int
    
class SetLastMeter(BaseModel):
    personal_account: int


# @app.get("/", summary="Получить все лицевые счета")
# async def get_all_account():
#     async with async_session() as session: 
#         query = select(MeterReading)
#         result = await session.execute(query)
#         meters = result.scalars().all()
#         return meters

# Обработчик POST-запроса
@app.post("/")
async def handle_post_request(move_meter: MoveMeter):
    # Проверяем наличие записи с указанным personal_account
    async with async_session() as session:
        result = await session.execute(
            select(MeterReading).where(MeterReading.personal_account == move_meter.personal_account)
        )
        meter_record = result.scalars().first()

        if not meter_record:
            raise HTTPException(status_code=404, detail="Record not found")

        # Обновляем значение meter
        meter_record.meter = move_meter.meter
        await session.commit()  # Сохраняем изменения
        await session.refresh(meter_record)  # Обновляем объект из базы

    # Возвращаем успешный ответ
    return {"message": "Meter updated successfully", "meter": meter_record.meter}

# Обработчик GET-запроса

@app.get("/")
async def handle_get_request(last_meter: SetLastMeter):
    # Проверяем наличие записи с указанным personal_account
    async with async_session() as session:
        result = await session.execute(
            select(MeterReading).where(MeterReading.personal_account == last_meter.personal_account)
        )
        meter_record = result.scalars().first()

        if not meter_record:
            raise HTTPException(status_code=404, detail="Record not found")


    # Возвращаем успешный ответ
    return {"meter": meter_record.meter, "personal_account": meter_record.personal_account}

