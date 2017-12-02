import datetime
import random

currentTime = datetime.datetime.now()

if currentTime.hour < 12:
    greeting_time = 'Good morning'
elif 12 <= currentTime.hour < 17:
    greeting_time = 'Good afternoon'
else:
    greeting_time = 'Good evening'

greeting_list = ["Hi Deepak, " + greeting_time, "Hello Deepak, "+ greeting_time,
                     "Hi Deepak, " + greeting_time + " Good to see you,I am your travel guide.",
                     "Hi Deepak, " + greeting_time + "I am glad to help you. Where would you like to go today?",
                     "Hi Deepak, " + greeting_time + " Where would you like to go today?"]

print(len(greeting_list))
print(greeting_list[random.randint(0, len(greeting_list)-1)])
