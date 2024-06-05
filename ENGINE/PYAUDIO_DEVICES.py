import pyaudio

def find_mic_id():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
            if p.get_device_info_by_host_api_device_index(0, i).get('name').find('HyperX Quadcast') != -1:
                print('MIC IS A HYPERX QUADCAST:')
                return i