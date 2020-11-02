from pynput import keyboard
import time
import pickle

WORDS = "just staying one day ahead of yesterday"

digraph = dict()
pressing_time = dict() # {key: [t0,t1,t2,...]}

typing = ""
total_time = 0
k = None
prev_k = None
press_time = None
release_time = None

def on_press(key):
    global press_time, k, prev_k, typing, total_time

    # enter to start 
    if total_time == None or key == keyboard.Key.enter:
        total_time = time.clock() 
        print("start", total_time)   
    try:
        if key == keyboard.Key.space:
            print(" ", end="")
            typing += " "    
        else:
            print(key.char, end="")
            typing += key.char
        k = key
        prev_press_time = press_time
        press_time = time.time()
    
        # collect keypair time
        if prev_k != None and prev_press_time != None:
            pair_interval = press_time - prev_press_time
            digraph[(prev_k,key)] = digraph.get((prev_k,key), []) + \
                [pair_interval]
        # 
        prev_k = key
    except AttributeError:
        pass

def on_release(key):
    global release_time, press_time, k, prev_k, total_time

    # enter to start
    if key == keyboard.Key.enter:
        return

    # calculate time 
    release_time = time.time()
    interval = release_time - press_time
    # collect time (single keystroke)
    pressing_time[k] = pressing_time.get(k, []) + [interval]

    if typing == WORDS or key == keyboard.Key.esc:
        total_time = time.clock() - total_time
        print("end", total_time)
        return False # exit

def cal_mean():
    global digraph, pressing_time, total_time

    for k,v in digraph.items():
        digraph[k] = sum(v)/len(v)

    for k,v in pressing_time.items():
        pressing_time[k] = sum(v)/len(v)
    
    return digraph,pressing_time,total_time

if __name__ == "__main__":
    print("Please type the following sentence:")
    print(WORDS)
    print("press enter to start")
    total_time = time.time()
    with keyboard.Listener(
        on_press = on_press,
        on_release = on_release) as listener: 
        listener.join()
    cal_mean()
    print(digraph)
    print('###')
    print(pressing_time)
    print(total_time)
    save_dict = {**digraph, **pressing_time}
    save_dict['total']= total_time
    with open('times.pickle', "wb") as f:
        pickle.dump(save_dict,f)
