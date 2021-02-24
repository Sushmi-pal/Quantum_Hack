from django.apps import AppConfig
from django.conf import settings

import os
import pickle
import joblib as jb
class AiConfig(AppConfig):
    name = 'AI'

    path = os.path.join(settings.MODELS,'trained_model')

    with open(path,'rb') as pickled:
        model = jb.load(pickled)
