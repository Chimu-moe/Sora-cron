from database import SQL, REDIS
import json

try:
    REDIS.ping()
except:
    print("Failed to connect to redis! a connection is required...")


# Get current position for the current day. this cron runs every day ONCE!
users = SQL.query("SELECT Id FROM Users")
for user in users:
    user_lb = SQL.query("SELECT * FROM Leaderboard WHERE id = %s LIMIT 1", (user['Id']))
    
    for mode in [0,1,2,3]:
        key = f"sora:performance:{user['Id']}_{mode}"
        last = REDIS.get(key)
        if last == None:
            last = []
        else:
            last = json.loads(last)
        
        if (len(last) >= 60):
            last.pop(0)

        position = 0
        
        if mode == 0:
            position = SQL.query("SELECT COUNT(PerformancePointsOsu > PerformancePointsOsu) as position FROM Leaderboard WHERE Id = %s", user['Id'])[0]['position']
        elif mode == 1:
            position = SQL.query("SELECT COUNT(PerformancePointsOsu > PerformancePointsOsu) as position FROM Leaderboard WHERE Id = %s", user['Id'])[0]['position']
        elif mode == 2:
            position = SQL.query("SELECT COUNT(PerformancePointsOsu > PerformancePointsOsu) as position FROM Leaderboard WHERE Id = %s", user['Id'])[0]['position']
        elif mode == 3:
            position = SQL.query("SELECT COUNT(PerformancePointsOsu > PerformancePointsOsu) as position FROM Leaderboard WHERE Id = %s", user['Id'])[0]['position']

        last.append(position) # Next Position
        REDIS.set(key, json.dumps(last))
