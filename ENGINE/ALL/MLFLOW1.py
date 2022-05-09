import os
from random import random, randint
from mlflow import log_metric, log_param, log_artifacts

if __name__ == "__main__":
    # Log a parameter (key-value pair)
    log_param("param1", randint(0, 100))

    # Log a metric; metrics can be updated throughout the run
    log_metric("foo", random())
    log_metric("foo", random() + 1)
    log_metric("foo", random() + 2)

    # Log an artifact (output file)
    if not os.path.exists("../DIRS/AI/MLOPS/outputs"):
        os.makedirs("../DIRS/AI/MLOPS/outputs")
    with open("../DIRS/AI/MLOPS/outputs/test.txt", "w") as f:
        f.write("hello world!")
    log_artifacts("../DIRS/AI/MLOPS/outputs")
