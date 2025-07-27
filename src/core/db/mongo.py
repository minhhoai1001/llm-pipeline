from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from core.config import settings

class MongoDBClient:
    """Singleton class to connect to MongoDB database."""
    
    _instance: MongoClient | None = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(settings.MONGO_DATABASE_HOST)
                # logger.info(
                #     f"Connection to database with uri: {settings.MONGO_DATABASE_HOST} successful"
                # )
            except ConnectionFailure:
                # logger.error(f"Couldn't connect to the database.")

                raise

        return cls._instance

    def get_database(self):
        assert self._instance, "Database connection not initialized"

        return self._instance[settings.MONGO_DATABASE_NAME]

    def close(self):
        if self._instance:
            self._instance.close()
            
mongoClient = MongoDBClient()