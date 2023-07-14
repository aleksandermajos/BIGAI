import torch

def detect_gpu_pytorch():
    print(torch.__version__)
    print('IS GPU AVAILABLE? :')
    print(torch.cuda.is_available())
    print('HOW MANY DEVICES? :')
    print(torch.cuda.device_count())
    for i in range(torch.cuda.device_count()):
        print(torch.cuda.get_device_name(i))

detect_gpu_pytorch()
