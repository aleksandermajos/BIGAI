from pathlib import Path
p = Path.cwd()
path_beginning = str(p.home())+'/PycharmProjects/EDENAI/'

def provide_key():
    f = open(path_beginning+"account.txt", "r")
    return(f.read())