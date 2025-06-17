from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def eeg_handler(addr, *values):
    print(addr, values)

disp = Dispatcher()
disp.map("/muse/eeg", eeg_handler)          # adapt path as needed
server = BlockingOSCUDPServer(("0.0.0.0", 5000), disp)
print("Listening on UDP 5000 …")
server.serve_forever()
