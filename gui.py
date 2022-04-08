import tkinter as tk

root = tk.Tk()
main_frame = tk.Frame(master=root)
chat_listbox = tk.Listbox(master=main_frame, height=200, width=50)
scroll_bar = tk.Scrollbar(master=main_frame)
speak_button = tk.Button(master=root, text='Command', command=lambda: None)
mic_button = tk.Button(master=root, text='Mic Switch', command=lambda: None)


def set_speak_command(command):
    speak_button.configure(command=command)
def set_mic_command(command):
    mic_button.configure(command=command)


speak_button.pack(side=tk.LEFT, anchor=tk.NW)
mic_button.pack(side=tk.LEFT, anchor=tk.NW)


def speak(text):
    chat_listbox.insert('end', f'Assistant: {text}')
def show(text):
    chat_listbox.insert('end', text)


scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
chat_listbox.pack(fill=tk.Y, side=tk.RIGHT)
scroll_bar.configure(command=chat_listbox.yview)
chat_listbox.configure(yscrollcommand=scroll_bar.set)
main_frame.pack(fill=tk.BOTH)
root.geometry('400x200')
root.minsize(400, 200)
root.wm_title('PING')
root.resizable(False, True)
mainloop = root.mainloop
