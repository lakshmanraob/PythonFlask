import datetime
import random
import time
from datetime import timezone
import os

currentTime = datetime.datetime.now()
curTime = time.time()
os.environ["TZ"] = "Asia/Kolkata"
time.tzset()
print(time.strftime("%H", time.localtime(curTime)))

hour = int(time.strftime("%H", time.localtime(curTime)))

if hour < 12:
    greeting_time = 'Good morning'
elif 12 <= hour < 17:
    greeting_time = 'Good afternoon'
else:
    greeting_time = 'Good evening'

greeting_list = ["Hi Deepak, " + greeting_time, "Hello Deepak, " + greeting_time,
                 "Hi Deepak, " + greeting_time + " Good to see you,I am your travel guide.",
                 "Hi Deepak, " + greeting_time + "I am glad to help you. Where would you like to go today?",
                 "Hi Deepak, " + greeting_time + " Where would you like to go today?"]

print(len(greeting_list))
print(greeting_list[random.randint(0, len(greeting_list) - 1)])
