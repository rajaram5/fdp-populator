import os
print("Hello this is FDP populator script")
DEMO_KEY = os.environ['DEMO_KEY']
count = int(DEMO_KEY) + 10
print("count :" + str(count))