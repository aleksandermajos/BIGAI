s = '07:05:45PM'

from datetime import *

def timeConversion1(s):
    if s[-2:] == "AM" and s[:2] == "12":
        return "00" + s[2:-2]
    elif s[-2:] == "AM":
        return s[:-2]
    elif s[-2:] == "PM" and s[:2] == "12":
        return s[:-2]
    else:
        ans = int(s[:2]) + 12
        return str(str(ans) + s[2:8])

def timeConversion2(s):
    return str(int(s[:2])%12+(0 if s[-2]=="A" else 12)).zfill(2)+s[2:8]

def timeConversion3(s):
    input_time = datetime.strptime(s, "%I:%M:%S%p")
    return input_time.strftime("%H:%M:%S")

if __name__ == '__main__':
    #n = int(input())
    timeConversion1(s)
    timeConversion2(s)
    timeConversion3(s)