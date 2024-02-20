from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/HF/'

def provide_key():
    f = open(path_beginning+"token.txt", "r")
    return(f.read())