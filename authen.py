import pickle
import numpy as np
import time

from sklearn.neighbors import KNeighborsClassifier

from typing import List
from pynput import keyboard
from keyrecode import *

def load_data(user_folder:str, keys:List):
    user_times = []
    for i in range(1,6):
        with open("./{}/times{}.pickle".format(user_folder,i),"rb")\
            as f:
            tmp = pickle.load(f)
        times = []
        for key in keys:
            times.append(tmp[key])
        user_times.append(times)
    return user_times

def knn(u1, u2, new_data):
    x =  u1 + u2
    y = [0,0,0,0,0,1,1,1,1,1]
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(x, y)
    if neigh.predict([new_data])[0] == 0:
        print("user1")
    else:
        print("user2")
    
    print(
        "predict proba for both user is", 
        neigh.predict_proba([new_data])
        )

if __name__ == "__main__":
    
    print("Please type the following sentence:")
    print(WORDS)
    print("press enter to start")
    start_time = time.time()
    with keyboard.Listener(
        on_press = on_press,
        on_release = on_release) as listener: 
        listener.join()
    di,single,total=cal_mean()
    save_dict = {**di, **single}
    print(f"total time is %f" % total)
    save_dict['total'] = total
    
    
    # fix key
    with open("./user1/times1.pickle", "rb") as f:
        tmp = pickle.load(f)
        keys = list(tmp.keys())
        # print(keys) #

    # print(save_dict)
    new_data = []
    for key in keys:
        new_data.append(save_dict[key])
    user1 = load_data("user1", keys)
    user2 = load_data("user2", keys)
    
    knn(user1,user2,new_data)