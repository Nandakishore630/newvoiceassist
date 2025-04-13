import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import requests
import os
import subprocess
import webbrowser
from googlesearch import search
from thefuzz import fuzz
 


wake_words = ["janu", "juni", "jannu","june"]

def is_similar(wake_command, keywords, threshold=80):
    """
    Check if the recognized word is similar to any wake words.
    """
    for word in keywords:
        if fuzz.ratio(wake_command, word) >= threshold:
            return True
    return False
# speech recognizer and text-to-speech engine
listener = sr.Recognizer()
machine = pyttsx3.init()
voices = machine.getProperty("voices")



machine.setProperty("voice", voices[2].id)
# TO make the assistant speak
def talk(text):
    print(f"Janu: {text}")
    machine.say(text)
    machine.runAndWait()


# Function to listen and recognize speech
listener = sr.Recognizer()  

def input_instruction():
    try:
        with sr.Microphone() as origin:
            print("🎤 Listening...")
            listener.adjust_for_ambient_noise(origin, duration=1)  # Reduce for background noise
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech).lower()  # Convert text to lowercase
            print(f"✅ Recognized: {instruction}")
            return instruction

    except sr.UnknownValueError:
        print("❌ Could not understand the speech.")
        return ""
    except sr.RequestError:
        print("❌ Could not connect to speech recognition service.")
        return ""
    except Exception as e:
        print(f"❌ Error: {e}")
        return ""



# Function to get the weather report
def get_weather(city="Mumbai"):
    api_key = "5c15c2beeea649758c435828250203"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    response = requests.get(url).json()

    if "error" in response:
        print("❌ Error: Invalid city name or API key.")
        return
    
    weather = response['current']['condition']['text']
    temp = response['current']['temp_c']
    humidity = response['current']['humidity']
    wind_speed = response['current']['wind_kph']
    #talk(temp)
    print(f"✅ Weather in {city}: {weather}")
    print(f"🌡 Temperature: {temp}°C")
    print(f"💧 Humidity: {humidity}%")
    print(f"💨 Wind Speed: {wind_speed} km/h")



def google_search(query):
    """Search Google and open the top result in Chrome."""
    try:
        talk(f"Searching Google for {query}...")
        results = list(search(query, num_results=3))  
        
        if results:
            top_result = results[0]  
            talk(f"Opening the top result: {top_result}")
            print(f"Opening: {top_result}")
        
            webbrowser.open(top_result)
            talk("I will wait. Say 'Janu' when you're ready to continue.")
            
            #Wait until the wake word is spoken
            while True:
                wake_command = input_instruction().lower()
                if is_similar(wake_command, wake_words):
                    talk("I'm listening again!")
                    break
                elif "exit" in wake_command or "stop" in wake_command:
                    talk("Goodbye! Have a great day.")
                    return
                else:
                    talk("Please repeat.")
        else:
            talk("Sorry, no search results found.")
    except Exception as e:
        talk("Sorry, I couldn't perform the search.")
        print("Error:", e)


def get_news():
    """Fetches general latest news."""
    try:
        api_key = "111d1a00b2524d4cafd98ef37c378e72"
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        
        response = requests.get(url).json()
        if 'articles' in response and response['articles']:
            articles = response['articles'][:5]  # Fetch top 5 headlines
            talk("Here are the latest news headlines:")
            for article in articles:
                print(article['title'])
                talk(article['title'])
        else:
            talk("Sorry, I couldn't find any news.")
    except Exception as e:
        talk("Sorry, I couldn't fetch the news.")
        print("Error:", e)

def get_news_about_area(area_name):
    """Fetches news about a specific area or location."""
    try:
        api_key = "111d1a00b2524d4cafd98ef37c378e72" 
        url = f"https://newsapi.org/v2/everything?q={area_name}&sortBy=publishedAt&apiKey={api_key}"
        
        response = requests.get(url).json()
        if 'articles' in response and response['articles']:
            articles = response['articles'][:5]  # Fetch top 5 articles
            talk(f"Here are the latest news headlines about {area_name}:")
            for article in articles:
                print(article['title'])
                talk(article['title'])
        else:
            talk(f"Sorry, I couldn't find any news about {area_name}.")
    except Exception as e:
        talk("Sorry, I couldn't fetch the news.")
        print("Error:", e)


# Function to control system commands
def system_control(command):
    if "shutdown" in command:
        talk("Are you sure you want to shut down the system? Say yes or no.")
        confirmation = input("Confirm shutdown? (yes/no): ").lower()

        if confirmation == "yes":
            talk("Shutting down the system.")
            os.system("shutdown /s /t 5")
        else:
            talk("Shutdown canceled.")

    elif "restart" in command:
        talk("Are you sure you want to restart the system? Say yes or no.")
        confirmation = input("Confirm restart? (yes/no): ").lower()

        if confirmation == "yes":
            talk("Restarting the system.")
            os.system("shutdown /r /t 5")
        else:
            talk("Restart canceled.")

    elif "log out" in command:
        talk("Are you sure you want to log out? Say yes or no.")
        confirmation = input("Confirm logout? (yes/no): ").lower()

        if confirmation == "yes":
            talk("Logging out.")
            os.system("shutdown -l")
        else:
            talk("Logout canceled.")

            

# Function to open applications
def open_application(app_name):
    apps = {
        "notepad": "notepad.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "vs code": "C:\\Users\\nanda\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    }
    if app_name in apps:
        talk(f"Opening {app_name}")
        subprocess.Popen(apps[app_name])
    else:
        talk("Application not found.")



def is_junu_called(word):
    """Check if the recognized word is close to 'Junu'."""
    match = difflib.get_close_matches(word,wake_words , n=1, cutoff=0.7)
    return bool(match)
# Function to execute commands

def play_janu():
    unknown_count = 0
    talk("Welcome! How can I assist you?")
    while True:
        instruction = input_instruction().lower()

        if "play" in instruction or "song" in instruction:
            song = instruction.replace("play", "").strip()
            talk(f"Playing {song}. I will stop listening until the song ends.")
            
            # Play song and wait until user calls "Junu"
            pywhatkit.playonyt(song)
            talk("Song is playing. Say 'Janu' when you're ready to continue.")

            while True:
                wake_command = input_instruction().lower()
                if is_similar(wake_command, wake_words):
                    talk("I'm listening again!")
                    break
                elif "exit" in wake_command or "stop" in wake_command:
                    talk("Goodbye! Have a great day.")
                    return
                else:
                    talk("Please repeat.")

        elif "time" in instruction:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f'Current time is {current_time}')

        elif "date" in instruction:
            current_date = datetime.datetime.now().strftime('%d-%m-%Y')
            talk(f"Today's date is {current_date}")
        elif "janu" in instruction or "what is your name" in instruction or "your name" in instruction:
            talk("I am Janu... What can I do for you?")

        elif "how are you" in instruction:
            talk("I am fine, how about you?")
        
        

        elif "who is" in instruction:
            try:
                person = instruction.replace("who is", "").strip()
                info = wikipedia.summary(person, sentences=1)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                talk(f"Too many results found for {person}. Please be more specific.")
            except wikipedia.exceptions.PageError:
                talk(f"I couldn't find information on {person}.")
        
        
        elif "weather" in instruction:
            talk("Which city's weather would you like to know?")
            city = input_instruction().strip()
            if city:
                print(f"Fetching weather for: {city}")
                get_weather(city)
            else:
                talk("I didn't get the city name. Please try again.")

        elif "search" in instruction or "google" in instruction:
            query = instruction.replace("search", "").replace("google", "").strip()
            if query:
                google_search(query)
            else:
                talk("What would you like to search for?")
                query = input_instruction().strip()
                google_search(query)



        elif "news" in instruction:
            words = instruction.split()
            if len(words) > 1:  # 
                area_name = " ".join(words[1:])  # Extract the area name after "news"
                get_news_about_area(area_name)
            else:
                get_news()

        elif "open" in instruction:
            app_name = instruction.replace("open", "").strip()
            open_application(app_name)

        elif "shutdown" in instruction or "restart" in instruction or "log out" in instruction:
            system_control(instruction)

        elif any(word in instruction for word in ["exit", "stop", "end", "close", "bye"]):
            talk("Goodbye! Have a great day.")
            exit() 
        else:
            unknown_count += 1
            talk("I didn't understand. Please repeat.")

            if unknown_count >4:
                talk("I'm unable to understand. Exiting now.")
                break

play_janu()
