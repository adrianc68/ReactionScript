import time
import re
import pyperclip
import os
import cronometer
import func_timer
import pygame


LOG_FILE_PATH = ("/Users/angeladrian/Library/Application Support/minecraft/logs/latest.log")
LOG_UNSCRAMBLES = True
time_for_reaction = 18

def send_macro(text): 
    pyperclip.copy(text)

def unscrable_word(after_reaction):
    def extract_string(text, start_string, end_string):
        pattern = rf"{re.escape(start_string)}(.*?){re.escape(end_string)}"
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None

    def check_string_match(file_path, search_string):
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if sorted(search_string) == sorted(line) and len(search_string) == len(
                    line
                ):
                    return line
        return None

    unscrambles_file = "unscrambles.txt"
    start_string = "Unscramble the word "
    end_string = " for a random prize!"
    extracted_string = extract_string(after_reaction, start_string, end_string)
    if extracted_string:
        print("Extracted string:", extracted_string)
        matched_word = check_string_match(unscrambles_file, extracted_string)

        if matched_word:
            send_macro(matched_word)
        else:
            print("No matching word found in the unscrambles file")
    else:
        print("No matching string found in the provided string")

def solve_expression(after_reaction):
    start_string = "Solve the expression "
    end_string = " for a random prize!"
    start_index = after_reaction.find(start_string) + len(start_string)
    end_index = after_reaction.find(end_string)

    if start_index != -1 and end_index != -1:
        expression = after_reaction[start_index:end_index]
        expression = expression.replace("x", "*")
        result = eval(expression)
        if "*" in expression:
            send_macro(str(result))
        else:
            send_macro(str(result))

def type_word(after_reaction):
    start_string = "Type the word "
    end_string = " for a random prize!"
    start_index = after_reaction.find(start_string) + len(start_string)
    end_index = after_reaction.find(end_string)

    if start_index != -1 and end_index != -1:
        desired_word = after_reaction[start_index:end_index]
        send_macro(desired_word)


def log_unscrambles(after_reaction):
    start_string = " unscrambled the word "
    end_string = " in "
    if start_string in after_reaction and end_string in after_reaction:
        start_index = after_reaction.find(start_string) + len(start_string)
        end_index = after_reaction.find(end_string)

        if start_index != -1 and end_index != -1:
            logged_word = after_reaction[start_index:end_index]
            if not os.path.isfile("unscrambles.txt"):
                open("unscrambles.txt", "a").close()
            with open("unscrambles.txt", "r") as file:
                lines = file.readlines()
            if logged_word + "\n" not in lines:
                with open("unscrambles.txt", "a") as file:
                    file.write(logged_word + "\n")
                print(f"The word '{logged_word}' was added to the file.")
            else:
                print(f"The word '{logged_word}' already exists in the file.")

def start_timers():
    cronometer.restart_cronometer()
    func_timer.restart(time_for_reaction, play_sound_and_clear_clipboard)


def read_chat_log():
    with open(LOG_FILE_PATH, "r") as log_file:
        log_file.seek(0, 2) 
        while True:
            new_line = log_file.readline()
            if not new_line:
                time.sleep(0.1) 
                continue
            # if '[CHAT]' in new_line and new_line.startswith("Reaction » "): 
            if "[CHAT]" in new_line:

                chat_message = new_line.split("[CHAT]")[1].strip()
                # print(chat_message)
                if "Reaction » " in chat_message:
                    after_reaction = chat_message.split("Reaction » ", 1)[1]
                    if after_reaction.startswith("Unscramble"):
                        unscrable_word(after_reaction)
                        start_timers()
                    elif after_reaction.startswith("Type"):
                        type_word(after_reaction)
                        start_timers()
                    elif after_reaction.startswith("Solve"):
                        solve_expression(after_reaction)
                        start_timers()
                    else:
                        log_unscrambles(after_reaction)

def play_sound_and_clear_clipboard():
    pygame.mixer.init()
    pygame.mixer.music.load("alerta.wav")
    pygame.mixer.music.play()

    send_macro("t")


read_chat_log()
