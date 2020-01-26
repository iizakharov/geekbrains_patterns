import logging
import asyncio
from datetime import datetime
import motor.motor_asyncio
from interfaces import DatabaseInterface

logger = logging.getLogger('Database')


class Users(DatabaseInterface):
    def __init__(self):
        client = motor.motor_asyncio.AsyncIOMotorClient()
        db = client.users_database
        self.collection = db.users_collection

    async def create_or_update(self, user, is_active=True):
        filter_ = {
            "telegram_id": user['id']
        }
        user['is_active'] = is_active
        update_ = {
            "$set": user,
            "$currentDate": {
                "updatedAt": True  # set field updatedAt to current date automagically. Good practice ;)
            },
            "$setOnInsert": {
                "createdAt": datetime.utcnow()
                # set field createdAt to current date automagically ONLY IF it's a new record
            }

        }
        result = await self.collection.update_one(filter_, update_, upsert=True)
        logger.info(f'Create user: {result}')

    async def remove(self, id):
        filter_ = {
            "telegram_id": id
        }
        await self.collection.delete_many(filter_)

    async def get(self, id):
        filter_ = {
            "telegram_id": id
        }
        projection_ = {
            "_id": False  # don't return the _id
        }
        document = await self.collection.find(filter=filter_, projection=projection_)
        logger.debug(f'Found: {document}')
        return document

    async def activate(self, user):
        await self.create_or_update(user, True)

    async def deactivate(self, user):
        await self.create_or_update(user, False)
    

class Movies(DatabaseInterface):
    def __init__(self):
        super().__init__()
        logger.debug('Users db was created')

    async def create_or_update(self):
        pass

    # def update(self):
    #     pass

    async def remove(self):
        pass

    async def get(self):
        pass

    async def activate(self):
        pass

    async def deactivate(self):
        pass