import easytensor
import time
print(easytensor.upload_model(
    "my_model_"+str(time.time()),
    "/home/kamal/repos/python-client/my_model")
)
