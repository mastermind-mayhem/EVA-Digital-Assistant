import configparser  # isort: skip
import os  # isort: skip

import gui  # isort: skip
import speech_recognition as sr  # isort: skip
from actions import (  # isort: skip
    change_rate,
    change_voice,
    change_volume,
    search_engine_selector,
    set_gui_speak,
    speak,
    set_gui_show,
    show,
    wish_me
    # wish_me_bye
)
from commands import (  # isort: skip
    command_hello,
    command_nothing,
    command_open,
    command_search,
    command_whatsup,
    command_wikipedia,
    command_echo
)
import datetime
import getpass
import os
import random
import smtplib
import sys
import webbrowser
    # cd onedrive/documents/github/desktopassistant
    # python jarvis2_4windows.py
popular_websites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "wikipedia": "https://www.wikipedia.org",
    "amazon": "https://www.amazon.com",
    "github": "https://www.github.com",
}

romeo = """
Two households, both alike in dignity,
In fair Verona, where we lay our scene,
From ancient grudge break to new mutiny,
Where civil blood makes civil hands unclean.
From forth the fatal loins of these two foes
A pair of star-cross'd lovers take their life;
Whose misadventured piteous overthrows
Do with their death bury their parents' strife.
The fearful passage of their death-mark'd love,
And the continuance of their parents' rage,
Which, but their children's end, nought could remove,
Is now the two hours' traffic of our stage;
The which if you with patient ears attend,
What here shall miss, our toil shall strive to mend.
"""

def main(search_engine, take_command, debug):
    def execute_the_command_said_by_user():

        show('Testing')
        query = take_command()


        # logic for executing commands without arguments
        phrases = {
            "what's up": command_whatsup,
            "nothing": command_nothing,
            "exit": command_nothing,
            "stop": command_nothing,
            "hello": command_hello,
            "echo": command_echo,
        }
        for phrase, command in phrases.items():
            if phrase in query:
                command()

        # logic for executing commands with arguments
        if "wikipedia" in query:
            command_wikipedia(speak, debug, query)

        elif "open" in query:
            command_open(
                query,
                popular_websites,
                debug,
                search_engine,
                take_command
            )

        elif "search" in query:
            command_search(query, search_engine)

        elif "mail" in query:
            command_mail(take_command)

        elif "change rate" in query:
            change_rate(query, take_command)

        elif "change voice" in query.lower():
            change_voice(query, take_command)

        elif "change volume" in query.lower():
            change_volume(query, take_command)

        elif "date" in query:
            speak(f"The date is {datetime.datetime.now():%A, %B %d, %Y}")

        elif "time" in query:
            speak(f"The time is {datetime.datetime.now():%I %M %p}")
        speak("-------------------")
        # speak("Next Command! Sir!")
    def mic_change():
        try:
            mic = config['DEFAULT']['mic']
            if mic == 'False':
                config['DEFAULT']['mic'] = 'True'
                speak('I detected that the mic was off')
            elif mic == 'True':
                config['DEFAULT']['mic'] = 'False'
                speak('I detected that the mic was on')
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        except Exception:
            speak("Invalid value. Please try again.")

    gui.set_speak_command(execute_the_command_said_by_user)
    gui.set_mic_command(mic_change)
    set_gui_speak(gui.speak)
    set_gui_show(gui.show)
    gui.mainloop()


def run():
    master = config['DEFAULT']['master']

    search_engine = search_engine_selector(config)

    mic = config['DEFAULT']['mic']
    debug = config['DEFAULT']['debug']
    def take_command():
        mic = config['DEFAULT']['mic']
        debug = config['DEFAULT']['debug']
        if mic == "False":
            return input("Input: ")
        else:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening....")
                r.pause_threshold = 0.5
                r.energy_threshold = int(config['DEFAULT']['energy_threshold'])
                audio = r.listen(source)

            query = " "
            try:
                print("Recognizing....")
                query = r.recognize_google(audio, language="en-in")
                show("user said: " + query)
                # userspeak(query)

            except sr.UnknownValueError:
                if debug == "True":
                    print("Sorry Could You please try again")
                else:
                    pass
                speak("Sorry Could You please try again")

            except Exception as e:
                if debug == "True":
                    print(e)
                    print("Say That Again Please")
                else:
                    pass
            # query = input("Input: ")

            return query
    speak("Initializing PING")
    wish_me(master)
    if mic == "True":
        speak('The Microphone is on')
    else:
        speak('The Microphone is off')
    main(search_engine, take_command, debug)


if os.path.isfile('./config.ini'):  # Checks if config.ini exists.
    config = configparser.ConfigParser()  # if exists loads library.
    config.read('config.ini')  # and also the file.
    run()  # Then it launches the main program
else:
    # if it doesn't exist it drops an error message and exits.
    print('You need a config.ini file.')
    print('Check the documentation in the Github Repository.')
