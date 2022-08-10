import torch

import numpy as np

print('Pytorch version:', torch.__version__)

a = [1,2,3]
b= np.array([4,5,6], dtype=np.int32)

t_a = torch.tensor(a)
t_b = torch.from_numpy(b)

print(torch.is_tensor(a))
print(torch.is_tensor(b))

t_ones = torch.ones(2,3)
t_ones.shape
print(t_ones)

rand_tensor = torch.rand(2,3)
print(rand_tensor)

t_a_new = t_a.to(torch.int64)
print(t_a_new.dtype)

t = torch.rand(3,5)
t_tr = torch.transpose(t,0,1)
print(t.shape, '-->', t_tr.shape)

t = torch.zeros(30)
t_reshape = t.reshape(5,6)
print(t_reshape)

t = torch.zeros(1,2,1,4,1)
t_sqz = torch.squeeze(t,2)
print(t.shape, '-->', t_sqz.shape)

torch.manual_seed(1)
t1 = 2*torch.rand(5,2) -1
t2 = torch.normal(mean=0,std=1, size=(5,2))
t3 = torch.multiply(t1,t2)
print(t3)

t4 = torch.mean(t1, axis=0)
print(t4)

t5 = torch.matmul(t1, torch.transpose(t2,0,1))
print(t5)
t6 = torch.matmul(torch.transpose(t1,0,1), t2)
print(t6)

norm_t1 = torch.linalg.norm(t1, ord=2, dim=1)
print(norm_t1)

torch.manual_seed(1)
t= torch.rand(6)
t_splits = torch.chunk(t,3)
[item.numpy() for item in t_splits]

A= torch.ones(3)
B= torch.zeros(3)
C=torch.cat([A,B], axis=0)
S=torch.stack([A,B],axis=1)








