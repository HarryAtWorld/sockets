from datetime import datetime
import time

def save_log(message):

    dt = datetime.now()
    file_name = f"./log/{dt.year}-{dt.month}-{dt.day}.txt"


    try:
        with open(file_name, "a") as log:
            log.write(f"{dt}    {message}.\n")
    except BaseException as err:
        print(err)

save_log("1st")

time.sleep(3)

save_log("2nd")