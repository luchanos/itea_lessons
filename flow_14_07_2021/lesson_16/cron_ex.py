import datetime

f_path = "/flow_14_07_2021/lesson_16/test.txt"

with open(f_path, "a") as f_o:
    f_o.write(str(datetime.datetime.now()))
