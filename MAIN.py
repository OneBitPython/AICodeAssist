import nltk
from nltk.tokenize import sent_tokenize
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pywhatkit
import datetime
import webbrowser
import wikipedia
import pyjokes
import wolframalpha
import pyttsx3
import time
from playsound import playsound
import speech_recognition as sr
import random
import keyboard
import pandas as pd


client = wolframalpha.Client('AEQLPR-9HWU85XHK6')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')


def get_audio():
    playsound("Siri_Sound_Effect_HD.mp3")
    r = sr.Recognizer()
    print("Listening...")
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print("USER:" + said)
        except Exception as e:
            speak("Im sorry, I didn't get you.")
            said = input("Do you want to type in the command? ")

    return said


def speak(audio):
    print("COMPUTER: " + audio)

    try:
        audio = audio.split('https')
    except:
        pass

    if len(audio[0]) > 450:
        speak(
            "\nThe message was extremely long so I didnt read it out aloud, I will wait for 15 seconds so you can go through the article")
        time.sleep(15)
        speak("Hope you are done reading it.")
    else:
        engine.say(audio[0])
        engine.runAndWait()


print(
    "Basic Instructions\n-------------------------------------------------------------------\n1. For better results, try without writing 'in python'..\n2. You can say change voice to male and change to voice to female to change voice of the model.\n3. For resources just say the word 'resources'.\n4 'Table of contents' is another keyword you can use to recieve all the topics taught in order.\n5. Say 'features' to get a list of available features\n6. You can also ask me to sleep.\n\n")
with open('dialogs.txt') as f:
    output = f.read()

tokens = sent_tokenize(output)

lemmers = nltk.stem.WordNetLemmatizer()


def lemmatizer(every_token):
    return [lemmers.lemmatize(token) for token in every_token]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def tokenize(text):
    return lemmatizer(nltk.word_tokenize(text.lower()))


def chat():
    while True:
        text = get_audio()

        chatbot = ''
        tokens.append(text)

        TfidfVec = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
        tfidf = TfidfVec.fit_transform(tokens)

        vals = cosine_similarity(tfidf[-1], tfidf)

        values = vals.argsort()[0][-2]

        flat = vals.flatten()
        flat.sort()

        req_tfidf = flat[-2]

        if req_tfidf == 0:
            if 'your name' in text:
                speak("My name is ChattyBotty and I help you break down hard topics.")
            elif 'change voice to female' in text:
                engine.setProperty('voice', voices[1].id)
                speak("Changed voice to female")
            elif 'change voice to male' in text:
                engine.setProperty('voice', voices[0].id)
                speak("Changed voice to male")
            elif 'how are you' in text:
                speak("Doing well, thanks")
            elif 'my name' in text:
                speak("Not sure")
            elif 'are you' in text:
                speak("My name is ChattyBotty and I help you break down hard topics.")
            elif 'bye' in text or 'see you' in text or 'goodbye' in text:
                speak('GOODBYE')
                break
            else:
                print("Results from my companion-WolframAlpha, please wait.")
                try:
                    res = client.query(text)
                    output = next(res.results).text
                    speak(output)

                    speak("I hope that this is the answer that you had expected.")
                except:
                    speak("Hmmmm, that\'s hard to answer.")

        else:
            try:
                speak(tokens[values])

                ans = tokens[values]
                ans = ans.lower()

                tokens.remove(text)

                text = text.lower()
                if 'sleep' in ans:
                    print("PRESS (SHIFT+S) TO WAKE ME UP")
                    keyboard.wait("shift+s")
                    akn = ["I'm Online Boss",
                           "I'm with you", "i'm ready"]
                    speak(random.choice(akn))
                    text = ""

                if 'change voice to male' in text:
                    engine.setProperty('voice', voices[0].id)
                    speak("Changed voice to male")
                if 'change voice to female' in text:
                    engine.setProperty('voice', voices[1].id)
                    speak("Changed voice to female")
                if 'whatsapp' in text:
                    try:
                        date = datetime.datetime.now()

                        hour = date.strftime("%H")
                        tmin = date.strftime("%M")

                        tmin = int(tmin) + 2

                        tell = speak("What do you want the content of the message to be?")
                        message = get_audio()
                        tell2 = speak("Who should I send the whatsapp message to (number)")
                        number = input("Who should I send the whatsapp message to (number) : ")
                        pywhatkit.sendwhatmsg("+91" + number, str(message), int(hour), tmin)

                        speak("Sure, I will send this whatsapp message")
                    except:
                        pass

                if 'open youtube' in text:
                    webbrowser.open('www.youtube.com')

                if 'gmail' in text:
                    webbrowser.open('https://mail.google.com/')

                if 'outlook' in text:
                    webbrowser.open('https://outlook.live.com/')

                if 'playing video on youtube' in ans:
                    say = speak('What do you want me to play')
                    what_to_play = get_audio()
                    pywhatkit.playonyt(what_to_play)

                if 'text on google' in ans:
                    tell4 = speak("What do you want to search for?")
                    subject = get_audio()
                    pywhatkit.search(subject)

                if 'wikipedia' in text or 'wiki' in text:
                    goto = speak("What do you want to search for on wikipedia : ")
                    subject = get_audio()
                    try:
                        answer = wikipedia.summary(subject, sentences=2)

                        speak(f'\n{answer}')
                        webbrowser.open(f'https://en.wikipedia.org/wiki/{subject}')

                    except:
                        webbrowser.open(f'https://en.wikipedia.org/wiki/{subject}')
                        print("\nThere was an error. So we directly took you to the wikipedia site.\n")

                if 'music' in ans:
                    webbrowser.open(
                        'https://www.amazon.in/music/prime?ref_=dmm_acq_marin_d_bra_zzz_jkBWTRVw-dc_c_335004885047')

                if 'joke' in ans:
                    speak(pyjokes.get_joke())

                if 'quora' in ans:
                    try:
                        say = speak("What do you want to search for on quora")
                        what = get_audio()
                        what = what.lower()

                        ans = what.split(' ')

                        final = ''
                        for i in ans:
                            final += i
                            final += '-'

                        webbrowser.open(f'https://www.quora.com/{final[0:-1]}')
                    except:
                        pass
            except:
                pass


chat()


