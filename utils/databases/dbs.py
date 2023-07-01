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

key5 = os.getenv('MONGODBSTORIESKEY')
cluster5 = motor.motor_asyncio.AsyncIOMotorClient(key5)
stories_database = cluster5['Askro']  # Stories

key6 = os.getenv('MONGODBINTROSKEY')
cluster6 = motor.motor_asyncio.AsyncIOMotorClient(key6)
intros_database = cluster6['Askro']  # Intros

key7 = os.getenv('MONGODBBIRTHDAYSKEY')
cluster7 = motor.motor_asyncio.AsyncIOMotorClient(key7)
birthdays_database = cluster7['Askro']  # Birthdays