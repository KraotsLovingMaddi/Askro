import os
import motor.motor_asyncio


key1 = os.getenv('MONGODBLEVELSKEY')
cluster1 = motor.motor_asyncio.AsyncIOMotorClient(key1)
levels_database = cluster1['Askro']  # Levels

key2 = os.getenv('MONGODBMUTESKEY')
cluster2 = motor.motor_asyncio.AsyncIOMotorClient(key2)
mutes_database = cluster2['Askro']  # Mutes

key3 = os.getenv('MONGODBMARRIAGESKEY')
cluster3 = motor.motor_asyncio.AsyncIOMotorClient(key3)
marriages_database = cluster3['Askro']  # Marriages

key4 = os.getenv('MONGODBMISCKEY')
cluster4 = motor.motor_asyncio.AsyncIOMotorClient(key4)
misc_database = cluster4['Askro']  # Misc