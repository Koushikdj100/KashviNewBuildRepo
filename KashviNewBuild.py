import webbrowser
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import re
import datetime
import time
from selenium import webdriver
import ctypes
from tkinter import *
import tkinter as tk
import threading
from os import path
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def takeuserinput(lang='kn', msg='Listening...'):
    with sr.Microphone() as source:
        r = sr.Recognizer()
        print(msg)
        display(msg, 2)
        r.pause_threshold = 0.6
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            display("Recognizing......", 2)
            query = r.recognize_google(audio, language=f'{lang}-IN')
            print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            clear_display(heading_text2)
            display("Please only speak when I am listening", 2)
            print("Please only speak when I am listening", e)
            return ""
    return query

def say(music):
    playsound(music)

def etks(text, id=1):
    current_path = os.getcwd()
    dir = os.path.join(current_path, 'music', f'eng{id}.mp3')
    if not os.path.exists(current_path+'//music'):
        os.mkdir(current_path+'//music')
    kan_txt = text_translator(text, 'kn')
    print("Kannada text",kan_txt )
    display(kan_txt, 4)
    obj = gTTS(text=kan_txt, slow=False, lang='kn')
    if(os.path.exists(dir)):
        os.remove(dir)
    obj.save(dir)
    say(dir)
    os.remove(dir)


def text_translator(text, dest='kn'):
    try:
        from googletrans import Translator
        translator = Translator()
        translation = translator.translate(text, dest=dest)
        translate_text = translation.text
        return translate_text
    except:
        try:
            print("Trying to use Second translator as fallback")
            from translate import Translator
            toLang = 'English' if dest == 'en' else 'Kannada'
            translator = Translator(to_lang=toLang)
            print("Text to translate", text);
            translation = translator.translate(text)
            return translation
        except:
            print("Trying to use third translator as fallback")
            from google_trans_new import google_translator
            translator = google_translator()
            translate_text = translator.translate(text, lang_tgt=dest)
            return translate_text

commands = {
    'time': ['ಟೈಮ್', 'ಟೈಮ್ ಎಷ್ಟು', 'ಗಂಟೆ ಎಷ್ಟು', 'ಟೈಮೆಷ್ಟು', 'ಸಮಯ ಎಷ್ಟು', 'ಸಮಯವೆಷ್ಟು'],

    'google': ['ಗೂಗಲ್ ಅನ್ನು ತೆರೆಯಿರಿ', 'ಗೂಗಲ್ ತೆರೆ', 'ಗೂಗಲ್ ಓಪನ್', 'ಓಪನ್ ಗೂಗಲ್'],
    'map': ['ಮ್ಯಾಪ್','ಮ್ಯಾಪ್ಸ್','ನಕ್ಷೆ'] ,
    'twitter':['ಟ್ವಿಟರ್ ತೆರೆ','ಟ್ವಿಟರ್ ಓಪನ್','ಓಪನ್ ಟ್ವಿಟರ್','ಟ್ವಿಟರ್'],
    'facebook':['ಓಪನ್ ಫೇಸ್ಬುಕ್','ಫೇಸ್ಬುಕ್ ಓಪನ್','ಫೇಸ್ಬುಕ್ ತೆರೆ','ತೆರೆ ಫೇಸ್ಬುಕ್','ಎಫ್ಬಿ'],
    'instagram':['ಇನ್ಸ್ಟಾಗ್ರಾಮ್ ಓಪನ್','ಓಪನ್ ಇನ್ಸ್ಟಾಗ್ರಾಮ್','ತೆರೆ ಇನ್ಸ್ಟಾಗ್ರಾಮ್','ಇನ್ಸ್ಟಾಗ್ರಾಮ್ ತೆರೆ','ಓಪನ್ ಇನ್ಸ್ಟಾ'
        ,'ಇನ್ಸ್ಟಾ ಓಪನ್','ಇನ್ಸ್ಟಾಗ್ರಾಂ'],
    'flipkart':['ಫ್ಲಿಪ್ಕಾರ್ಟ್ ಓಪನ್','ಓಪನ್ ಫ್ಲಿಪ್ಕಾರ್ಟ್','ತೆರೆ ಫ್ಲಿಪ್ಕಾರ್ಟ್','ಫ್ಲಿಪ್ಕಾರ್ಟ್ ತೆರೆ','ಫ್ಲಿಪ್ಕಾರ್ಟ್','ಫ್ಲಿಪ್ಕರ್ಟ್','ಫ್ಲಿಪ್ಕಕರ್ಟ್'],
    'amazon':['ಅಮೆಜಾನ್ ಓಪನ್','ಓಪನ್ ಅಮೆಜಾನ್','ತೆರೆ ಅಮೆಜಾನ್','ಅಮೆಜಾನ್ ತೆರೆ','ಅಮೆಜಾನ್','ಯಮಝೋನ್'],
    'restart': ['ರೀಸ್ಟಾರ್ಟ್ ಕಂಪ್ಯೂಟರ್','ಕಂಪ್ಯೂಟರ್ ರೀಸ್ಟಾರ್ಟ್', 'ಗಣಕಯಂತ್ರವನ್ನು ಮರು ಪ್ರಾರಂಭಿಸು',
                'ಗಣಕಯಂತ್ರವನ್ನು ಮರುಪ್ರಾರಂಭಿಸಿ','ರೀಸ್ಟಾರ್ಟ್'],
    'sleep': ['ಗಣಕಯಂತ್ರವನ್ನು ಮಲಗಿಸು', 'ಗಣಕಯಂತ್ರ ಮಲಗು','ಕಂಪ್ಯೂಟರ್ ಮಲಗು','ಕಂಪ್ಯೂಟರ್ ಮಲಗಿಸು',
                'ಸ್ಲೀಪ್ ಕಂಪ್ಯೂಟರ್', 'ಕಂಪ್ಯೂಟರ್ ಸ್ಲೀಪ್', 'ಮಲಗು','ಸ್ಲೀಪ್'],
    'poweroff': ['ಕಂಪ್ಯೂಟರ್ ಕೆಡಿಸು', 'ಕಂಪ್ಯೂಟರ್ ಆರಿಸು', 'ಗಣಕಯಂತ್ರವನ್ನು ಆರಿಸು', 'ಗಣಕಯಂತ್ರವನ್ನು ಕೆಡಿಸು',
                  'ಶಟ್ ಡೌನ್ ಕಂಪ್ಯೂಟರ್', 'ಕಂಪ್ಯೂಟರ್ ಶಬ್ದೊನ್', 'ಕಂಪ್ಯೂಟರನ್ನು ಆರಿಸು','ಪವರ್ ಆಫ್'],
    'positive-statements': ['ಹೌದು', 'ಹಾ', 'ಎಸ್', 'ಓಕೆ'],
    'negative-statements': ['ನೋ', 'ಇಲ್ಲ', 'ಅಲ್ಲ']
}

def tweak_power(command, action):
    etks(f"Are you sure want to {action} computer")
    if testifarrayinline(commands['positive-statements'], takeuserinput('kn')):
        etks(f"Now computer will {action}")
        os.system(command)
    else:
        etks(f"Computer will not {action} due to your action or inaction")

# driver  =None
def open_google_maps(url):
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options)
    driver.get(url)
    time.sleep(5)
    button = driver.find_element(By.CSS_SELECTOR,"button#searchbox-searchbutton");
    button.click()
    time.sleep(2)
    button.click()

def search_word(arr, line):
    for elem in arr:
        if re.search(fr'({elem}+\s)|({elem}$)', line):
            return elem
    return None

def testifarrayinline(arr, line):
    for elem in arr:
        if re.search(fr'({elem}+\s)|({elem}$)', line):
            return True
    return False

def main():
    etks("namsthe, i am kashvi, how can i help you")
    display("namsthe, i am kashvi, how can i help you",1)
    while(1):
        msg = takeuserinput('kn', 'Listening to message')
        if search_word(commands['time'], msg):
            str= "Current time is : " + datetime.datetime.now().strftime("%H : %M ")
            etks(str)
            display(str,1)
        elif search_word(commands['twitter'], msg):
            etks("opening twitter")
            webbrowser.open_new("https://twitter.com")
        elif search_word(commands['facebook'], msg):
            etks("opening facebook")
            webbrowser.open_new("https://www.facebook.com")
        elif search_word(commands['instagram'], msg):
            etks("opening instagram")
            webbrowser.open_new("https://www.instagram.com")
        elif search_word(commands['google'], msg):
            etks("opening google")
            webbrowser.open_new("https://www.google.com")
        elif search_word(commands['flipkart'], msg):
            etks("opening flipkart")
            webbrowser.open_new("https://www.flipkart.com/")
        elif search_word(commands['amazon'], msg):
            etks("opening amazon")
            webbrowser.open_new("https://www.amazon.in/")
        elif search_word(commands['map'], msg):
            map_query = msg.replace(search_word(commands['map'], msg), '')
            open_google_maps(f"https://www.google.com/maps/place/{map_query}")
        elif search_word(commands['poweroff'],msg):
            # tweak_power("shutdown /s /t 1", 'power-off')
            os.system('shutdown /s /t 1')
        elif search_word(commands['restart'],msg):
            # tweak_power("shutdown /r /t 1", 'restart')
            os.system("shutdown /r /t 1")
        elif search_word(commands['sleep'],msg):
            # tweak_power("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", 'sleep')
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
                etks("say the sentace properly")


btheme ={
        'app-bg': '#22092C',
        'app-disp-bg': 'magenta',
        'n1-txt': 'white',
        'h1-txt': 'white',
        'h2-txt': 'white',
        'main-txt': 'white',
        'btn': {
            'start-bg': '#0275d8',
            'start-fg': 'white',
            'stop-bg': '#ff0000',
            'stop-fg': 'white',
            'rstart-bg': 'green',
            'rstart-fg': 'white',
        }
}

class thread_with_exception(threading.Thread):
    """
       This is a class to stop thread.
   """
    def __init__(self, func, name="Thread"):
        self.func = func
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        try:
            self.func()
        except Exception as e:
            print(e)

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        print(res, thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

def on_start():
    global t1, is_alive
    if not is_alive:
        display("Started", 1)
        clear_display(heading_text1, heading_text2, main_screen_text)
        if t1 is None:
            t1 = thread_with_exception(main, main)
            t1.daemon = True
            t1.start()
            is_alive = True
        elif t1 is not None:
            if not is_alive:
                t1 = thread_with_exception(main, main)
                t1.daemon = True
                t1.start()
                is_alive = True
            else:
                pass
    else:
        pass

def on_stop():
    global t1, is_alive
    if is_alive:
        clear_display(heading_text1, heading_text2, main_screen_text)
        display("Stopped, Press start", 1)
        display("Stopped", 2)
        display("Press start to start the program", 4)
        if t1 is not None:
            is_alive = False
            t1.raise_exception()
            t1 = None
    else:
        pass
def on_restart():
    on_stop()
    on_start()
    display("Restarted", 1)


def clear_display(*args):
    for elem in args:
        elem.set("")

def on_clear():
    clear_display(heading_text1, main_screen_text)

def display(value, choice):
    func_switcher = {
        1: notify_heading_text,
        2: heading_text1,
        3: heading_text2,
        4: main_screen_text,
    }
    disp_func = func_switcher.get(choice, " ")
    text_switcher = {
        1: "App has ",
        2: "Condition  :",
        3: "Input   : ",
        4: "Output  : ",
    }
    disp_text = text_switcher.get(choice, " ")
    disp_func.set(disp_text + value)

cur_theme = btheme
t1 = None
is_alive = False
root = Tk()
root.title('KASHVI')
windowWidth = 400
windowHeight = 600
print("Width", windowWidth, "Height", windowHeight)
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
root.geometry("400x600+{}+{}".format(positionRight, positionDown))
root.minsize(windowWidth, windowHeight)
main_screen_text = tk.StringVar()
heading_text1 = tk.StringVar()
heading_text2 = tk.StringVar()
notify_heading_text = tk.StringVar()
out_txt = "Press Start to Start program"

notification1 = Label(height=1, textvariable=notify_heading_text, bd=0)
notification1.pack(fill=X, side=TOP)
notification1.configure(bg=cur_theme['app-bg'], fg=cur_theme['n1-txt'], font=('Times New Roman', 12, 'bold'), pady=10)

heading1 = Label(height=1, wraplength=380, textvariable=heading_text1, bd=0)
heading1.pack(fill=X, side=TOP)
heading1.configure(bg=cur_theme['app-disp-bg'], fg=cur_theme['h1-txt'], font=('Times New Roman', 16, 'bold'), pady=10)

heading2 = Label(height=2, wraplength=380, textvariable=heading_text2, bd=0)
heading2.pack(fill=X, side=TOP)
heading2.configure(bg=cur_theme['app-disp-bg'], fg=cur_theme['h2-txt'], font=('Times New Roman', 12, 'bold'), pady=10)

main_screen = Label(height=14, wraplength=380, textvariable=main_screen_text, bd=0)
main_screen.pack(fill=BOTH, side=TOP, expand=TRUE)
main_screen.configure(bg=cur_theme['app-disp-bg'], fg=cur_theme['main-txt'], font=('Times New Roman', 12, 'bold'), pady=10)
main_screen_text.set(out_txt)

start_btn_txt = tk.StringVar()
start_btn = Button(root, borderwidth=0,  fg=cur_theme['btn']['start-fg'], activebackground='#025aa5',
                   activeforeground='white',
                   bg=cur_theme['btn']['start-bg'],text="Start",compound = RIGHT, command=on_start,
                   font=('Times New Roman', 12, 'bold'), padx=6, pady=6)
start_btn_txt.set('Start')
start_btn.pack(side=LEFT)

stop_btn_txt = tk.StringVar()
stop_btn = Button(root, borderwidth=0, fg=cur_theme['btn']['stop-fg'], activebackground='#ed0202',
                  activeforeground='white', bg=cur_theme['btn']['stop-bg'],
                  textvariable=stop_btn_txt, command=on_stop, font=('Times New Roman', 12, 'bold'), padx=6, pady=6,compound=RIGHT)
stop_btn_txt.set('Stop')
stop_btn.pack(side=LEFT, padx=60, pady=10)

restart_btn_txt = tk.StringVar()
restart_btn = Button(root,borderwidth=0, fg=cur_theme['btn']['rstart-fg'], activebackground='#40556a',
                     activeforeground='white', bg=cur_theme['btn']['rstart-bg'],
                     textvariable=restart_btn_txt, command=on_restart, font=('Times New Roman', 12, 'bold'), padx=6,
                     pady=6,compound=RIGHT)
restart_btn_txt.set('Restart')
restart_btn.pack(side=RIGHT)
root.configure(background=cur_theme['app-bg'], pady=10, padx=10)
root.mainloop()