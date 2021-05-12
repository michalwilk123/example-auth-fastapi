from motor import motor_asyncio
from app.config import MONGO_URL

mongo_client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db = mongo_client.cso

citizen_collection = db.citizens
auth_collection = db.auth