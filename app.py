from flask import Flask, request, make_response, jsonify
import re
from datetime import datetime
import time
from gtts import gTTS
import playsound
import requests as req
import random
app = Flask(__name__)

timeForm = ''
timeX = ''
wakeText = '' 
myAPIkey = '845346ee7c0b422bbf655b80995739ae'
sleepT = False
motivation = False 
def retrievenews():

    # sourcing
    sourcelist = ["techradar", "buzzfeed", "cnn", "hacker-news", "the-huffington-post", "time",]
    randomsource = sourcelist[random.randint(0, len(sourcelist) - 1)]

    """
    Addables / Parameters to put into link(add a ? or & ):
    category = categories(business, etc)
    sources = sourceInFormat
    q = subject
    """

    main_url = " https://newsapi.org/v1/articles?source=" + randomsource + "&sortBy=top&apiKey="+ myAPIkey

    # fetching data in json format
    open_webpage = req.get(main_url).json()

    # getting all articles in a string article
    # retrieves the articles from the full json set
    articlecollection = open_webpage["articles"]

    # empty list which will
    # contain all trending news
    results = []

    # in the collection of articles in JSON format collect the values linked to the key "title"
    for titleFinder in articlecollection:
        results.append(titleFinder["title"])

    if (randomsource == "cnn"):
        resultForSpeech = ("Source: " + "c n n" + "\n")
    else:
        resultForSpeech = ("Source: " + randomsource + "\n")

    # print out all the results in a loop
    for x in range(len(results)):
        # printing all trending news
        # print(x + 1, ")", results[x])
        resultForSpeech = resultForSpeech + (results[x]) + "\n"


    return resultForSpeech



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
        wakeText = "When the DNA of an organism changes and results in a new trait, it is known as a mutation." 
        wakeText+= " The first person to see a live cell with a microscope was Antonie van Leeuwenhoek, in 1674." 
        wakeText+= " Bacteria are extremely small and are made up of just one cell."
        wakeText+= " Animals that eat plants as their primary food source are known as herbivores"
        wakeText+= " Cats always land on their feet."
        wakeText+= " Female sharks have thicker skins than males."
        wakeText+= " The ocean is 8 empire state Buildings deep."

    elif (catagory == "News"):
        wakeText = retrievenews()
    elif(catagory == 'Motivational'):
        global motivation
        motivation = True
        wakeText = "N/a"

    else:
        wakeText = "Japanese square watermelons are ornamental plants and are not edible"
        wakeText+= " if you spin a ball as you drop it, it flies." 
        wakeText+= " most lipsticks contain fish scales."
        wakeText+= " recycling one glass jar saves enough energy to operate a television for three hours."
        wakeText+= " Leonardo Da Vinci invented scissors."
        wakeText+= " Horses can’t vomit."
        wakeText+= " slugs have four noses"
    
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
    global timeX 
    
    global sleepT
    data = request.get_json(silent=True)
    if(data.get('queryResult')['action'] == 'wake_choice'):
        if(data.get('queryResult').get('parameters')['wakeChoice'] == "Alarm"):
            return {"fulfillmentText": "Great, you want an Alarm. What time would you like your wake up call?"}
        else:
            sleepT = True
            return {"fulfillmentText": "Awesome, you choose a sleep timer. What is the category you would like?"}
    if(data.get('queryResult')['action'] == 'user_time'):
        x = make_response(jsonify(getTime()))
        timeX  = timeForm
        timeX  = datetime.strptime(timeX, "%H:%M:%S")
        return x 
    elif(data.get('queryResult')['action'] == 'wake_Catagory'):
        fact = catagory()
        alarm = gTTS(fact)
        alarm.save('alarm.mp3')
        print(sleepT)
    if(sleepT == False):
        while(checkTime(timeX) == False):
            time.sleep(30)
            if(checkTime(timeX) == True):
                break
    
    if(motivation == True):
        playsound.playsound('inspire.mp3', True)
        return "done"
    else:
        playsound.playsound('alarm.mp3',True)
        return fact
            
    

   






if __name__ == '__main__':
    app.run()