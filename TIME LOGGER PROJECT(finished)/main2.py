import json
import io
import datetime
import os

def export_to_json(*dicts):
    log_time=''+str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))+'.json'

    result={}

    for dct in dicts:
        result={**result,**dct}
    
    with open(log_time, 'w') as outfile:
        json.dump(result, outfile, indent=2)

def import_json_max_code():
    a=os.listdir()
    x=[]
    for i in a:
        if ".json" in i:
            x.insert(len(x), i)
    set_of_dates=set()
    max_code=0
    for i in x:
        with open(i, 'r') as f:
            value = json.load(f)
        code=value.pop("code",0)
        if code > max_code:
            max_code=code
    return max_code
def time_in_session(code_max):
    def import_json_info_code(code_max):
        files = [f for f in os.listdir() if f.endswith(".json")]
        sessions = []
        for filename in files:
            with open(filename, 'r') as f:
                data = json.load(f)
            if data.get("code") == code_max:
                start = data.get("start")
                stop = data.get("stop")
                if start and stop:
                    sessions.append((start, stop))
        return sessions

    def import_json_info_day():
        today = datetime.datetime.now().date()
        files = [f for f in os.listdir() if f.endswith(".json")]
        sessions = []
        for filename in files:
            with open(filename, 'r') as f:
                data = json.load(f)
            try:
                stop_dt = datetime.datetime.strptime(data["stop"], '%Y-%m-%d %H:%M:%S.%f')
                if stop_dt.date() == today:
                    start = data.get("start")
                    stop = data.get("stop")
                    if start and stop:
                        sessions.append((start, stop))
            except:
                continue
        return sessions

    # Time for matching code
    total_code_duration = datetime.timedelta()
    for start, stop in import_json_info_code(code_max):
        start_dt = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        stop_dt = datetime.datetime.strptime(stop, '%Y-%m-%d %H:%M:%S.%f')
        total_code_duration += (stop_dt - start_dt)

    # Time for today
    total_day_duration = datetime.timedelta()
    for start, stop in import_json_info_day():
        start_dt = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        stop_dt = datetime.datetime.strptime(stop, '%Y-%m-%d %H:%M:%S.%f')
        total_day_duration += (stop_dt - start_dt)

    return total_code_duration, total_day_duration


session_code=import_json_max_code()+1
quit_session=False
while not quit_session:
    new_dictionary={'code':session_code,'start':str(datetime.datetime.now())}
    print("new log info:   ",new_dictionary)
    quit_session=input("to Pause session enter blank, to quit sesion enter anythig:  ")
    new_dictionary["stop"]=str(datetime.datetime.now())
    print("full info about this log:  ",new_dictionary)
    export_to_json(new_dictionary)
    z=time_in_session(session_code)
    print("time spent in this sesion: ",z[0]," time spent today: ",z[1])
    



