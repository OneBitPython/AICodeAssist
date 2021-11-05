
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
import sys
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


print(
    "In a time where healthcare has been a majour concern I bring you the heart attack predictor,that does whatever the name implies it predicts if you have a heart attack or not based on 5 parameters.\n")

df = pd.read_csv('heart.csv')
df_raw = df[['age', 'sex', 'cp', 'fbs', 'chol', 'restecg']]

cp = input(
    "choose cp value, Value 0: typical angina, Value 1: atypical angina, Value 2: non-anginal pain, Value 3: asymptomatic : ")
cp = int(cp)

list_of_cp = [0, 1, 2, 3]
while cp not in list_of_cp:
    print("*Invalid")
    cp = input(
        "\nchoose cp value, Value 0: typical angina, Value 1: atypical angina, Value 2: non-anginal pain, Value 3: asymptomatic : ")
    cp = int(cp)

if cp == 0:
    cp_value = 'typical angina'
elif cp == 1:
    cp_value = 'atypical angina'
elif cp == 2:
    cp_value = 'non-anginal pain'
elif cp == 3:
    cp_value = 'asymptomatic'
else:
    pass

age = input("Age : ")
age = int(age)

while age <= 0 or age > 100:
    print("Invalid age")
    age = input("Age : ")
    age = int(age)

gender = input("Gender (1 for Male, 0 for Female) : ")
gender = int(gender)

genders = [0, 1]
while gender not in genders:
    print("*Invalid value")
    gender = input("Gender (1 for Male, 0 for Female)")
    gender = int(gender)

if gender == 0:
    gender_val = 'Female'
else:
    gender_val = 'Male'

fbs = input("Fasting blood sugar (mg/dl) : ")
fbs = int(fbs)

while fbs < 30 or fbs > 200:
    print("*Invalid")
    fbs = input("Fasting blood sugar (mg/dl) : ")
    fbs = int(fbs)

if fbs >= 120:
    fbs_val = 1
else:
    fbs_val = 0

chol = input("Cholestrol (mg/dl) : ")
chol = int(chol)

while chol > 500 or chol < 50:
    print("*Invalid cholestrol level")
    chol = input("Cholestrol (mg/dl) : ")
    chol = int(chol)

print(
    f"\n\nCP : {cp}-{cp_value}\nAGE : {age}\nGENDER : {gender}({gender_val})\nFBS (mg/dl) : {fbs}\nCHOL : {chol}\n")

model = DecisionTreeClassifier()

model.fit(df_raw[['age', 'sex', 'cp', 'fbs', 'chol']], df_raw['restecg'])

score = model.score(df_raw[['age', 'sex', 'cp', 'fbs', 'chol']], df_raw[['restecg']])
ans = model.predict([[age, gender, cp, fbs_val, chol]])

if ans[0] == 1:
    print("EMERGENCY!! You may have a heart attack consult a doctor.")
    playsound('Ambulance-sound-effect.mp3')

else:
    print("No problems at all.")
