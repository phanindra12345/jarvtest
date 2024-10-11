#heloo 
from bs4 import BeautifulSoup
import requests
from datetime import datetime  # Corrected import for the datetime class
import os
import re
import shutil  # For regular expressions
import psutil
import pyautogui
import pytz
import speech_recognition as sr  # Speech recognition library
import pyttsx3  # Text-to-speech conversion
import subprocess
import webbrowser
from playsound import playsound
import google.generativeai as genai
genai.configure(api_key=os.environ.get(
    "API_KEY", "AIzaSyAHR-VibLkLg15S99FvIWjr26UjeRz9dPQ"))


# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Function to make Jarvis speak


def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()


# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to take voice input and convert it to text with noise handling


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(
            source, duration=1)  # Adjust for ambient noise
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()  # Convert to lowercase for easier command processing
        except sr.UnknownValueError:
            speak("Sorry, I could not understand what you said. Please try again.")
            return ""
        except sr.RequestError:
            speak(
                "Sorry, I'm having trouble connecting to the speech recognition service.")
            return ""

# Function to respond to specific commands


def respond(command):
    # Remove any trigger word like "Jarvis"
    command = re.sub(r"\bjarvis\b", "", command).strip()
    if "create flutter project" in command:
        create_flutter_project()

    elif "push to github" in command:
        speak("Pushing code to GitHub.")
        result = git_push()
        speak(result)
        return False

    elif "commit" in command and "message" in command:
        match = re.search(r"commit with message\s+['\"]?(.*?)['\"]?$", command)
        if match:
            commit_message = match.group(1)
            speak(f"Committing changes with message: {commit_message}")
            result = git_commit(commit_message)
            speak(result)
            print(result)
        return False

    elif "add changes" in command:
        speak("Adding all changes.")
        result = git_add()
        speak(result)
        return False

    elif re.search(r"(hello|hi|hey)", command):
        speak("Hello! How can I assist you today?")
        return False
    elif re.search(r"(your name|who are you)", command):
        speak("I am Jarvis, your personal assistant.")
        return False

    elif re.search(r"time in (india|usa|uk|canada)", command):
        country = re.search(r"(india|usa|uk|canada)", command).group(0)
        current_time = get_current_time(country.upper())
        speak(f"The current time in {country.capitalize()} is {current_time}.")
        return False

    elif re.search(r"(open|start|launch)\s+(notepad|chrome|calculator|word)", command):
        app_name = re.search(
            r"(notepad|chrome|calculator|word)", command).group(0)
        speak(f"Opening {app_name}.")
        open_application(app_name)
        return False

    elif re.search(r"go to\s+(.*\..*)", command):
        website_name = re.search(r"go to\s+(.*\..*)", command).group(1)
        speak(f"Opening {website_name}.")
        open_website(website_name)
        return False

    elif re.search(r"copy\s+(.*)", command):
        text_to_write = re.search(r"copy\s+(.*)", command).group(1)
        speak(f"Writing '{text_to_write}' in Notepad.")
        write_in_notepad(text_to_write)
        return False

    elif re.search(r"close\s+(.*)", command):
        app_name = re.search(r"close\s+(.*)", command).group(1)
        speak(f"Closing {app_name}.")
        close_application(app_name)
        return False

    elif re.search(r"create a folder\s+(.*)", command):
        folder_name = re.search(r"create a folder\s+(.*)", command).group(1)
        create_folder(folder_name)
        return False

    elif "delete a folder" in command:
        match_delete = re.search(
            r"delete a folder\s+['\"]?(.+?)['\"]?$", command)
        if match_delete:
            folder_name = match_delete.group(1)
            delete_folder(folder_name)
        return False

    elif 'exit' in command or 'sleep' in command:
        speak("Putting the computer to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return True  # Exit the loop

    elif re.search(r"(play video song|play audio song)\s+(.*)", command):
        media_type = re.search(
            r"(play video song|play audio song)", command).group(1)
        song_name = re.search(
            r"(play video song|play audio song)\s+(.*)", command).group(2).strip()

        if "video song" in media_type:
            play_video_song(song_name)
        else:
            play_audio_song(song_name)
        return False

    elif "cpu usage" in command:
        speak(get_cpu_usage())
        return False
    elif "memory usage" in command:
        speak(get_memory_usage())
        return False
    elif "disc space" in command:
        speak(get_disk_space())
        return False
    elif command.startswith("ask gemini"):
        # Remove "ask gemini" from the command
        question = command.replace("ask gemini", "").strip()
        speak(f"Let me ask Gemini: {question}.")
        result = ask_gemini(question)  # Ask the Gemini AI the question
        print(result)  # Print the response from Gemini to the console
        # Make Jarvis speak the response
        return False

    # elif "create django project folder" in command:
    #     speak("Please tell me the name of the folder.")
    #     folder_name = listen()
    #     if folder_name:
    #         create_django_project(folder_name)
    #     return False
    elif "create project folder" in command:
        create_project_folder(command)
    elif "download" in command:
        speak("Please tell me the name of the application you want to download.")
        app_name = listen()
        if app_name:
           download_application(app_name)


    return None


# Function to get the current time for a specific country
def get_current_time(country):
    timezone_mapping = {
        'INDIA': 'Asia/Kolkata',
        'USA': 'America/New_York',  # Eastern Time Zone
        'UK': 'Europe/London',
        'CANADA': 'America/Toronto'  # Eastern Time Zone
    }

    tz = pytz.timezone(timezone_mapping[country])
    current_time = datetime.now(tz).strftime("%H:%M %p")  # Format time

    return current_time

# Function to open applications
def open_application(app_name):
    try:
        if 'notepad' in app_name:
            subprocess.Popen(['notepad.exe'])
        elif 'chrome' in app_name:
            subprocess.Popen(
                ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'])
        elif 'calculator' in app_name:
            subprocess.Popen(['calc.exe'])
        elif 'word' in app_name:
            subprocess.Popen(
                ['C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE'])
        else:
            speak("Sorry, I cannot open that application.")
    except FileNotFoundError:
        speak("The application was not found. Please check the installation.")
    except Exception as e:
        speak(f"Sorry, I encountered an error: {str(e)}")

# Function to open a website
def open_website(website_name):
    webbrowser.open(f"http://{website_name}")  # Open the website

# Function to write text in Notepad
def write_in_notepad(text):
    pyautogui.sleep(1)  # Adjust sleep time if necessary
    pyautogui.typewrite(text)  # Type the text into Notepad

# Function to close applications
def close_application(app_name):
    try:
        running_processes = {p.info['name'].lower(): p.info['pid']
                            for p in psutil.process_iter(['name', 'pid'])}
        matched_processes = [
            proc for proc in running_processes if app_name.lower() in proc]

        if matched_processes:
            for process in matched_processes:
                pid = running_processes[process]
                os.system(f"taskkill /f /pid {pid}")
                speak(f"{process.split('.')[0].capitalize()} has been closed.")
        else:
            speak(f"Sorry, no running application matches '{app_name}'.")
    except Exception as e:
        speak(
            f"Sorry, I encountered an error while closing {app_name}: {str(e)}")

# Function to create a folder on the desktop
def create_folder(folder_name):
    desktop_path = os.path.join(os.path.expanduser(
        "~"), "Desktop")  # Get the desktop path
    # Create the folder path
    folder_path = os.path.join(desktop_path, folder_name)

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # Create the folder
            speak(f"Folder '{folder_name}' has been created on your desktop.")
        else:
            speak(f"Folder '{folder_name}' already exists on your desktop.")
    except Exception as e:
        speak(
            f"Sorry, I encountered an error while creating the folder: {str(e)}")
        
# Function to delete a folder from the desktop
def delete_folder(folder_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop_path, folder_name)

    try:
        if os.path.exists(folder_path):
            # Use shutil.rmtree to delete the folder and its contents
            shutil.rmtree(folder_path)
            speak(
                f"Folder '{folder_name}' and its contents have been deleted from your desktop.")
        else:
            speak(f"Folder '{folder_name}' does not exist on your desktop.")
    except Exception as e:
        speak(
            f"Sorry, I encountered an error while deleting the folder: {str(e)}")

# Function to play video songs
# Function to play video songs
def play_video_song(song_name):
    search_url = f"https://www.youtube.com/results?search_query={'+'.join(song_name.split())}"
    speak(f"Searching for the video song '{song_name}' on YouTube.")
    webbrowser.open(search_url)  # Open the search results in a web browser

# Function to play audio songs
def play_audio_song(song_name):
    # Assuming you're using Spotify or another service; adjust the URL as needed
    search_url = f"https://open.spotify.com/search/{'+'.join(song_name.split())}"
    speak(f"Searching for the audio song '{song_name}' on Spotify.")
    webbrowser.open(search_url)  # Open the search results in a web browser

# Function to get the current CPU usage and stat
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)

    if cpu_usage < 50:
        state = "good"
    elif 50 <= cpu_usage <= 80:
        state = "average"
    else:
        state = "poor"

    return f"Current CPU usage is {cpu_usage}%. The CPU is in a {state} state."

# Function to get the current memory usage and state
def get_memory_usage():
    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    if memory_usage < 50:
        state = "good"
    elif 50 <= memory_usage <= 80:
        state = "average"
    else:
        state = "poor"

    return f"Current memory usage is {memory_usage}%. The memory is in a {state} state."

# Function to get the available disk space
def get_disk_space():
    disk = psutil.disk_usage('/')
    total_space = disk.total // (2**30)  # Convert to GB
    used_space = disk.used // (2**30)    # Convert to GB
    free_space = disk.free // (2**30)    # Convert to GB

    return f"Total disk space: {total_space}GB, Used: {used_space}GB, Free: {free_space}GB."
# Function to run git commands
def run_git_command(command):
    try:
        result = subprocess.run(
            command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error running git command: {e.stderr.decode('utf-8')}"

# Function to add changes


def git_add():
    return run_git_command("git add .")

# Function to commit changes with a voice-provided message


def git_commit(commit_message):
    print({commit_message})
    return run_git_command(f'git commit -m "{commit_message}"')
    

# Function to push to GitHub


def git_push():
    return run_git_command("git push origin main")  # or another branch


def ask_gemini(prompt):
    try:
        # Using the "gemini-1.5-flash" model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text if response and response.text else "I couldn't get a response."
    except Exception as e:
        return f"An error occurred with Gemini AI: {str(e)}"


# def create_django_project(folder_name):
#     desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
#     project_folder_path = os.path.join(desktop_path, folder_name)

#     try:
#         if not os.path.exists(project_folder_path):
#             os.makedirs(project_folder_path)  # Create the project folder
#             speak(f"Folder '{folder_name}' has been created on your desktop.")
#         else:
#             speak(f"Folder '{folder_name}' already exists on your desktop.")

#         # Install virtualenv
#         speak("Installing virtualenv.")
#         subprocess.run(["pip", "install", "virtualenv"], check=True)

#         # Ask for virtual environment name
#         speak("Please tell me the name of the virtual environment.")
#         venv_name = listen()
#         if venv_name:
#             venv_path = os.path.join(project_folder_path, venv_name)

#             # Create the virtual environment
#             subprocess.run(["virtualenv", venv_path], check=True)
#             speak(f"Virtual environment '{venv_name}' has been created.")

#             # Activate the virtual environment
#             activate_command = os.path.join(venv_path, "Scripts", "activate")
#             speak(f"Activating virtual environment '{venv_name}'.")
#             subprocess.call(activate_command, shell=True)

#             # Install Django
#             speak("Installing Django.")
#             subprocess.run(["pip", "install", "django"], check=True)

    #         # Start Django project
    #         speak("Please tell me the name of the Django project.")
    #         project_name = listen()
    #         if project_name:
    #             subprocess.run(["django-admin", "startproject",
    #                         project_name], cwd=project_folder_path, check=True)
    #             speak(f"Django project '{project_name}' has been created.")

    #             # Start Django app
    #             speak("Please tell me the name of the Django app.")
    #             app_name = listen()
    #             if app_name:
    #                 subprocess.run(["python", "manage.py", "startapp", app_name], cwd=os.path.join(
    #                     project_folder_path, project_name), check=True)
    #                 speak(f"Django app '{app_name}' has been created.")
    # except subprocess.CalledProcessError as e:
    #     speak(f"Sorry, an error occurred: {str(e)}")

def create_project_folder(command):
    speak("Please tell me the name of the folder.")
    folder_name = listen()
    if not folder_name:
        return

    # Ask for project type
    speak("What type of project is this? Please say Django, Flutter,  etc.")
    project_type = listen()

    if project_type:
        project_type = project_type.lower()  # Normalize to lower case

        if "django" in project_type:
            create_django_project(folder_name)
        elif "flutter" in project_type:
            # Assuming you have this function defined
            create_flutter_project(folder_name)
        else:
            speak("Sorry, I don't recognize that project type. Please try again.")
    else:
        speak("I didn't catch the project type. Operation canceled.")


def get_user_input(prompt):
    """Helper function to get user input with retry and close option."""
    while True:
        speak(prompt)
        user_input = listen()
        if user_input:
            if user_input.lower() == "close":
                speak("Operation has been canceled.")
                return None
            return user_input
        else:
            speak("I didn't catch that. Please repeat.")


def create_django_project(folder_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    project_folder_path = os.path.join(desktop_path, folder_name)

    try:
        if not os.path.exists(project_folder_path):
            os.makedirs(project_folder_path)  # Create the project folder
            speak(f"Folder '{folder_name}' has been created on your desktop.")
        else:
            speak(f"Folder '{folder_name}' already exists on your desktop.")

        # Install virtualenv
        speak("Installing virtualenv.")
        subprocess.run(["pip", "install", "virtualenv"], check=True)

        # Ask for virtual environment name
        venv_name = get_user_input(
            "Please tell me the name of the virtual environment.")
        if not venv_name:
            return  # Exit if the user cancels

        venv_path = os.path.join(project_folder_path, venv_name)

        # Create the virtual environment
        subprocess.run(["virtualenv", venv_path], check=True)
        speak(f"Virtual environment '{venv_name}' has been created.")

        # Activate the virtual environment
        activate_command = os.path.join(venv_path, "Scripts", "activate")
        speak(f"Activating virtual environment '{venv_name}'.")
        subprocess.call(activate_command, shell=True)

        # Install Django
        speak("Installing Django.")
        subprocess.run(["pip", "install", "django"], check=True)

        # Start Django project
        project_created = False  # Flag to track project creation status
        while not project_created:
            project_name = get_user_input(
                "Please tell me the name of the Django project.")
            if not project_name:
                return  # Exit if the user cancels

            try:
                subprocess.run(["django-admin", "startproject",
                               project_name], cwd=project_folder_path, check=True)
                speak(f"Django project '{project_name}' has been created.")
                project_created = True  # Set flag to True if project creation is successful
            except subprocess.CalledProcessError as e:
                speak(
                    f"Sorry, an error occurred while creating the project: {str(e)}")

        # Start Django app
        app_name = get_user_input("Please tell me the name of the Django app.")
        if not app_name:
            return  # Exit if the user cancels

        subprocess.run(["python", "manage.py", "startapp", app_name], cwd=os.path.join(
            project_folder_path, project_name), check=True)
        speak(f"Django app '{app_name}' has been created.")

        # Final success message
        speak("Django project and app creation completed successfully.")

    except subprocess.CalledProcessError as e:
        speak(f"Sorry, an error occurred: {str(e)}")


def create_flutter_project():
    # Ask the user for the project name
    project_name = input("Enter the name of the Flutter project: ")

    # Create the Flutter project using the provided name
    try:
        subprocess.run(['flutter', 'create', project_name], check=True)
        print(f"Flutter project '{project_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Flutter project. Error: {e}")


def search_application(app_name):
    # Use a search API or web scraping to find application download links.
    # Example search URL
    search_url = f"https://www.duckduckgo.com/?q={app_name}+download"
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        # Extract all links that are HTTPS
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith("https://"):
                links.append(href)

        return links
    else:
        return []


def download_application(app_name):
    speak(f"Searching for {app_name}.")

    # Search for the application
    download_links = search_application(app_name)

    if download_links:
        # For this example, just take the first secure link
        url = download_links[0]  # You could add logic to choose the best link

        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                file_path = os.path.join(desktop_path, f"{app_name}.zip")

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                speak(f"{app_name} has been downloaded successfully.")
            else:
                speak(
                    f"Sorry, I couldn't download {app_name}. Please try again later.")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")
    else:
        speak(
            f"Sorry, I couldn't find any secure download links for {app_name}.")


if __name__ == "__main__":
    speak("Hello, I am Jarvis. How can I assist you today?")

    while True:
        # Listen for commands
        command = listen()

        # Check if the command includes a stop keyword to exit
        if command:
            exit_program = respond(command)  # Check if the user wants to exit

            if exit_program:  # Exit if the user said goodbye or sleep
                break

            # Handle unrecognized commands here
            if exit_program is None:  # Only respond if not exiting
                speak("I'm not sure how to help with that.")

