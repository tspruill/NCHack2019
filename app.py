from flask import Flask, request, make_response, jsonify
import re
from datetime import datetime
import time
from gtts import gTTS
import playsound
import random
app = Flask(__name__)

timeForm = ''
timeX = ''
wakeText = '' 

def getTime():
    data = request.get_json(silent=True)
    userResult = data.get('queryResult').get('parameters')['time']
    formatResult = re.split("(\d\d\:\d\d\:\d\d)",userResult)
    global timeForm
    dateTime = datetime.strptime(formatResult[1], "%H:%M:%S")
    timeForm = dateTime.strftime("%H:%M:%S")
    
    return {"fulfillmentText": "Great I will wake you up at " + timeForm + ". Now what catergory would you like to wake up to?"}

def catagory():
    global wakeText 
    data = request.get_json(silent=True)
    catagory = data.get('queryResult').get('parameters')['wake_Catagory']
    if(catagory == 'Science'):
        wakeText = "When the DNA of an organism changes and results in a new trait, it is known as a mutation" 

    elif (catagory == "New"):
        
    else:
        wakeText = "Japanese square watermelons are ornamental plants and are not edible"

    
    return  wakeText

def checkTime(timeC):
    print(datetime.now().hour)
    print(datetime.now().minute)
    if(timeC.hour == datetime.now().hour and timeC.minute == datetime.now().minute):
        return True
    else:
        return False 








@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    data = request.get_json(silent=True)
    if(data.get('queryResult')['action'] == 'user_time'):
        x = make_response(jsonify(getTime()))
        global timeX 
        timeX  = timeForm
        timeX  = datetime.strptime(timeX, "%H:%M:%S")
        return x 
    elif(data.get('queryResult')['action'] == 'wake_Catagory'):
        fact = catagory()
        alarm = gTTS(fact)
        alarm.save('alarm.mp3')
        print(checkTime(timeX))
        while(checkTime(timeX) == False):
            
            time.sleep(30)
            if(checkTime(timeX) == True):
                break
    playsound.playsound('alarm.mp3',True)
    return fact
            
    

   






if __name__ == '__main__':
    app.run()