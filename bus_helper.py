import time

import tkinter as tk
import tkinter.font as tkFont

import threading as thread
from queue import Queue
import sys
import os
import obde
from time import sleep
import TTS


''' input by keyboard '''
def get_bus_num (q) :
    while True :
        tmp = input("Input bus id : ")
        q.put(tmp)

''' ui '''
def update_UI (label, q) :
    bus_list = []
    
    while True :
        if q.empty() == False :
            tmp = q.get()
                
            if tmp[1] == True : # to delete
                if tmp[0] in bus_list :
                    bus_list.remove(tmp[0])                    
            else : # to append
                if tmp[0] in bus_list :
                    continue
                else :
                    bus_list.append(tmp[0])
    
            label["text"] = bus_list
def tts (q) :
    while True :
        if q.empty() == False :
            tmp = q.get()
            print(" ========== ", tmp," ========== ")

'''thread manager '''
def manage_thread(win, label) :
    OBDE = obde.BusDetection()
    k_q = Queue() # keyboard
    u_q = Queue() # UI
    t_q = Queue() # TTS
    
    monitor_thread = thread.Thread(target= update_UI, args= (label, u_q,), daemon= True)
    monitor_thread.start()
    keyboard_thread = thread.Thread(target= get_bus_num, args= (k_q,), daemon= True)
    keyboard_thread.start()
    speaker_thread = thread.Thread(target= TTS.tts, args= (t_q,), daemon= True)
    speaker_thread.start()
    webcam_thread = thread.Thread(target= OBDE.find_bus,  daemon= True)
    webcam_thread.start()
    while True :
        sleep(0.1)
        while k_q.empty() == False : # key board input
            from_k = k_q.get()
            u_q.put([from_k, False]) # to append
            OBDE.bus_number.put(from_k) # to append
        while OBDE.find_bus_number.empty() == False : # find bus
            from_o = OBDE.find_bus_number.get()
            u_q.put([from_o, True]) # to delete
            t_q.put(from_o)
#print("o tmp\n")

if __name__ == "__main__" :
    win = tk.Tk()  # UI assignment

    win.title("Test 1") # title name
    win.geometry('950x500+0+0') # length x width + locate from left + locate from top
    win.resizable(False, False) # unable to change window size

    label = tk.Label(win)

    label["fg"] = "blue"    # color
    text_info = tkFont.Font(family="Lucia Grande", size=30) # font style, font size
    label["font"] = text_info   # font
    label["text"] = ""

    label.pack()

    manage_thread = thread.Thread(target= manage_thread, args= (win, label,), daemon= True)
    manage_thread.start()

    win.mainloop()
