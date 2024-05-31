import asyncio
from db.connection import DatabaseOperation


async def main():
    db = DatabaseOperation()
    await db.connectPool()
    db.test()


asyncio.run(main())
