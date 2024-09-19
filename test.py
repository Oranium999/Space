import tkinter as tk 
import datetime 

def tick():
    showed_time = clock['text']
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if showed_time != current_time:
        showed_time = current_time
        clock.configure(text=current_time)
    global alarm #make sure the alarm is known
    alarm = clock.after(1000, tick)#assign the alarm to a variable
    return None
def stop():
    stop.after_cancel(alarm) #cancel alarm
    

root=tk.Tk()

clock = tk.Label(root)
clock.pack()
stop = tk.Button(root, text='Stop it!', command=stop)
stop.pack()
tick()


root.mainloop()