# %% STEP 1: import libraries
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

# %% STEP 2: Ignore any warning messages
warnings.filterwarnings('ignore')

#STEP 3: Record audio and return as a string
def recordAudio():
    # record audio
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Hello. I\'m Elsa. How can i help you?')
        audio = r.listen(source)
    
    # Speech recognition using Google's speech recognition:
    data = ''
    try:
        data = r.recognize_google(audio)
        print('you said: ' + data)
    except sr.UnknownValueError:
        print('Sorry i dont understand')
    except sr.RequestError:
        print('Sorry i dont understand')

    return data

#STEP 4: Get the virtual assistant response
def assistantResponse(text):
    print(text)

    # convert text to speech
    myObj = gTTS(text = text, lang = 'en', slow = False)

    # save audio to a file
    myObj.save('assistant_response.mp3')

    # play converted file
    os.system('start assistant_response.mp3')

#STEP 5: Check Wake words
def wakeWord(text):
    WAKE_WORDS = ['hey computer', 'hello computer']
    text = text.lower()

    # check to see if users command contains a wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    # if wake word was not found return false
    return False


'''
***************************************************
** CREATE BASIC FUNCTIONS FOR ASSISTANT, INCLUDING:
  - GREETING
  - GET DATE TIME
  - LOOK UP INFORMATION OF A PERSON ON WIKIPEDIA
***************************************************
'''

#STEP 6: Generate a random greeting response
def greeting(text):
    GREETING_INPUTS = ['hey', 'hello']
    GREETING_RESPONSE = ['hello', 'hi']

    for word in text:
        if word in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSE) + ' Nguyen.'
        
    return ''

#STEP 7: Get person's name
def getPerson(text):
    wordList = text.split()

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) -1 and wordList[i].lower() == 'who' and wordList[i + 1].lower == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]

#STEP 8: Get Date / Time
def getDate():
    now = datetime.datetime.now()
    monthNum = now.month
    dayNum = now.day

    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()] # return today, e.g: Monday

    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    ordinal_numbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th',                      
                      '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', 
                      '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
    
    return 'Today is ' + weekday + ' ' + month_names[monthNum - 1] + ' the ' + ordinal_numbers[dayNum - 1] + '.'
    
'''
***************************************************
** Main method
***************************************************
'''

#STEP 9: Main
while True:
    # record audio
    text = recordAudio()
    response = '' # empty response string

    # check for wake words:
    if(wakeWord(text) ==  True):
        # check greeting by user
        response = response + greeting(text)

        # check if user said about date
        if('date' in text):
            get_date = getDate()
            response = response + ' ' + get_date
        
        # check to see if the user said time
        if('time' in text):
            now = datetime.datetime.now()
            meridiem = ''
            if (now.hour >= 12):
                meridiem = 'p.m'
                hour = now.hour - 12
            else:
                meridiem = 'a.m'
                hour = now.hour
        
        # convert minute into string
            if now.minute < 10:
                minute = '0' + str(now.minute)
            else:
                minute = str(now.minute)

            response = response + ' ' + 'It is ' + str(hour) + ': ' + minute + ' ' + meridiem + '.'

        # check if user said about "who is "
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences = 5)
            response = response + ' ' + wiki

        assistantResponse(response)



# %%
