from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/HF/'

def provide_key():
    f = open(path_beginning+"account.txt", "r")
    return(f.read().strip())