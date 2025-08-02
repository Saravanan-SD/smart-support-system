import motor.motor_asyncio
from app.core.config import setting

client =motor.motor_asyncio.AsyncIOMotorClient(setting.MONGO_URI)

db= client[setting.MONGO_DB]
tickets_collection =db['tickets']