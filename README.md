# EasyTensor

The official python client for [EasyTensor](https://easytensor.com).

# Installation

Pretty straightforward.

```shell
pip install easytensor
```

# Usage
Once you have a model exported to your local storage, you can upload it to easytensor in one line of code.

### Exporting and uploading a model

```python
import easytensor
import os
export_path = os.path.join(os.getcwd(), "my_model")
print("export_path: {}".format(export_path))

# Export the model
tf.keras.models.save_model(
    model,
    export_path,
    overwrite=True,
    include_optimizer=True,
    save_format=None,
    signatures=None,
    options=None
)

# Upload it to easytensor.
model_id, access_token = easytensor.upload_model("My first model", export_path)
print("model ID:", model_id)
print("access token:", access_token)
```


### Running prediction on the cloud

```python
from pprint import pprint
import requests
response = requests.post(
    "https://app.easytensor.com/query/",
    json={
        "instances": [
            image_to_predict.numpy().tolist()
        ]
    },
    headers={"accessToken": access_token}
)
print("Response from server:")
pprint(response.json())
```

# Running Examples

The library comes with a few example Jupyter notebooks that walk you through a few possible workflows. They are helpful if you are starting out with ML or remote model prediction.

#### Requirements
- Tensorflow 2. TF2 currently (early 2021) [requires a python version 3.5-3.8](https://www.tensorflow.org/install). You will have to install a compatible version of python.
- virtualenv
- jupyter notebook


##### For Mac
```
brew install python@3.8
```

##### For Ubuntu
```
sudo apt install python3.8 python3.8-dev
```

To run the examples, create a python virtual env, and install jupyter notebook.
```bash
# install virtualenv
pip3 install virtualenv

# create a virtualenv with python3.8 in ~/virtualenv-3.8
virtualenv --python=$(which python3.8) ~/virtualenv-3.8

# activate the virtual env
source ~/virtualenv-3.8/bin/activate

# install jupyter notebook and necessary widgets
pip install notebook ipywidgets

# run jupyter notebook
jupyter notebook 
```

# Questions and Help
If you have any querstions about how EasyTensor works or want help with serving your ML model, please contact me directly at [kamal@easytensor.com](mailto:kamal@easytensor.com). I'm here to help!