import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))

tf.debugging.set_log_device_placement(True)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# Num GPUs Available:  1

tf.config.list_physical_devices('GPU')
# [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]

sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))