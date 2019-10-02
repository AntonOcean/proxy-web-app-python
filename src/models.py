from bson import ObjectId
from bson.errors import InvalidId


async def create_store_dump(db, data) -> (str, str):
    pass


async def get_store_dump(db, import_id: str) -> (dict, str):
    try:
        ObjectId(import_id)
    except (TypeError, InvalidId):
        return {}, "Invalid import_id"

    pass