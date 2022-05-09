import torch

def detect_gpu_pytorch():
    print('IS AVAILABLE? :')
    print(torch.cuda.is_available())
    print('HOW MANY DEVICES? :')
    print(torch.cuda.device_count())
    for i in range(torch.cuda.device_count()):
        print(torch.cuda.get_device_name(i))
        print('Allocated:', round(torch.cuda.memory_allocated(1) / 1024 ** 3, 1), 'GB')
        print('Cached:   ', round(torch.cuda.memory_reserved(1) / 1024 ** 3, 1), 'GB')
