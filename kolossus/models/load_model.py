
import torch
from .Network import Network

# note: very hacky, change to host on some website in the future 
import os
import sys 


MODEL_FILE = 'saved_model_cs_ws_ft_humansty.epoch_59.pth'
FILE_PATH = os.path.join(os.path.split(__file__)[0], MODEL_FILE)
FILE_HUGGINGFACE_URL = 'https://huggingface.co/aparekh2/kolossus/resolve/main/saved_model_cs_ws_ft_humansty.epoch_59.pth'


if not os.path.isfile(os.path.join(os.path.split(__file__)[0], MODEL_FILE)):
    print(f"Downloading model from {FILE_HUGGINGFACE_URL} to {FILE_PATH}.")
    torch.hub.download_url_to_file(FILE_HUGGINGFACE_URL, FILE_PATH)


def load_model():
    path = os.path.split(__file__)[0]
    model_weights = os.path.join(path, MODEL_FILE)
    model = Network()
    model.load_state_dict(torch.load(model_weights))
    return model 
