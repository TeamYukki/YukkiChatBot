#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/YukkiChatBot >.
#
# This file is part of < https://github.com/TeamYukki/YukkiChatBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiChatBot/blob/master/LICENSE >
#
# All rights reserved.
#

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from config import MONGO_DB_URI

db = None

if MONGO_DB_URI != None:
    mongo = MongoClient(MONGO_DB_URI)
    db = mongo.ChatBot

    usersdb = db.users
    blockeddb = db.block
    modedb = db.mode
    modelist = {}

    # Served Users
    async def is_served_user(user_id: int) -> bool:
        user = await usersdb.find_one({"user_id": user_id})
        if not user:
            return False
        return True

    async def get_served_users() -> list:
        users_list = []
        async for user in usersdb.find({"user_id": {"$gt": 0}}):
            users_list.append(user)
        return users_list

    async def add_served_user(user_id: int):
        is_served = await is_served_user(user_id)
        if is_served:
            return
        return await usersdb.insert_one({"user_id": user_id})

    # Banned Users
    async def get_banned_users() -> list:
        results = []
        async for user in blockeddb.find({"user_id": {"$gt": 0}}):
            user_id = user["user_id"]
            results.append(user_id)
        return results

    async def get_banned_count() -> int:
        users = blockeddb.find({"user_id": {"$gt": 0}})
        users = await users.to_list(length=100000)
        return len(users)

    async def is_banned_user(user_id: int) -> bool:
        user = await blockeddb.find_one({"user_id": user_id})
        if not user:
            return False
        return True

    async def add_banned_user(user_id: int):
        is_gbanned = await is_banned_user(user_id)
        if is_gbanned:
            return
        return await blockeddb.insert_one({"user_id": user_id})

    async def remove_banned_user(user_id: int):
        is_gbanned = await is_banned_user(user_id)
        if not is_gbanned:
            return
        return await blockeddb.delete_one({"user_id": user_id})

    # Forward Mode
    async def is_group() -> bool:
        chat_id = 123
        mode = modelist.get(chat_id)
        if not mode:
            user = await modedb.find_one({"chat_id": chat_id})
            if not user:
                modelist[chat_id] = False
                return False
            modelist[chat_id] = True
            return True
        return mode

    async def group_on():
        chat_id = 123
        modelist[chat_id] = True
        user = await modedb.find_one({"chat_id": chat_id})
        if not user:
            return await modedb.insert_one({"chat_id": chat_id})

    async def group_off():
        chat_id = 123
        modelist[chat_id] = False
        user = await modedb.find_one({"chat_id": chat_id})
        if user:
            return await modelist.delete_one({"chat_id": chat_id})

else:

    async def is_group() -> bool:
        return False

    async def is_banned_user(user_id: int) -> bool:
        return False

    async def add_served_user(user_id: int):
        return True
