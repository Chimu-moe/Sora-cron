import database

try:
    database.REDIS.ping()
except:
    print("Failed to connect to redis! a connection is required...")


