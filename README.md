# EasyTensor

This is the official python client for EasyTensor.

## Examples

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

