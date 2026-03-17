from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    """
    Connect to MongoDB — works identically with:
      - Local: mongodb://localhost:27017
      - Atlas: mongodb+srv://user:pass@cluster.mongodb.net
    
    Motor handles both connection formats automatically.
    Schema, queries, and API remain exactly the same.
    """
    logger.info(f"Connecting to MongoDB: {settings.MONGODB_URL[:30]}...")
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db_instance.db = db_instance.client[settings.DATABASE_NAME]

    # Verify connection
    try:
        await db_instance.client.admin.command("ping")
        logger.info(f"✅ Connected to MongoDB database: {settings.DATABASE_NAME}")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        raise

async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        logger.info("MongoDB connection closed.")

def get_database():
    return db_instance.db
