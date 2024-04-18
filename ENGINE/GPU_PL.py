import torch
import pytorch_lightning as pl

# Initialize PyTorch Lightning trainer (optional but recommended)
trainer = pl.Trainer()

# List all available GPUs
num_gpus = torch.cuda.device_count()
print("Available GPUs:")
for i in range(num_gpus):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")