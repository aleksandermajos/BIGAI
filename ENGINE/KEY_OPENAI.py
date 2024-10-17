from openai import OpenAI
import os
from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/OPENAI/'
path = path_beginning+""
cwd = os.getcwd()
f = open(path+"account.txt", "r")
key = f.read().strip()
client = OpenAI(api_key=key)

def provide_key():
    f = open(path_beginning+"account.txt", "r")
    return(f.read().strip())
