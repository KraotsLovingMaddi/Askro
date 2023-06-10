import os
import motor.motor_asyncio


key1 = os.getenv('MONGODBLEVELSKEY')
cluster1 = motor.motor_asyncio.AsyncIOMotorClient(key1)
database1 = cluster1['Askro']  # Levels

key2 = os.getenv('MONGODBMUTESKEY')
cluster2 = motor.motor_asyncio.AsyncIOMotorClient(key2)
database2 = cluster2['Askro']  # Mutes

key3 = os.getenv('MONGODBMARRIAGESKEY')
cluster3 = motor.motor_asyncio.AsyncIOMotorClient(key3)
database3 = cluster3['Askro']  # Marriages

key4 = os.getenv('MONGODBMISCKEY')
cluster4 = motor.motor_asyncio.AsyncIOMotorClient(key4)
database4 = cluster4['Askro']  # Misc