from django.shortcuts import render

from .apps import AiConfig

from django.http import JsonResponse
from rest_framework.views import APIView
from django.conf import settings

import os
import numpy as np

import pandas as pd 
# Create your views here.

def make_data(sample):
    path = os.path.join(settings.MODELS,'data/all_x.csv')

    X = pd.read_csv(path)
    total_columns = X.columns
    disease_idx={}
    for i,dis in enumerate(total_columns):
        disease_idx[dis] = i

    data = np.zeros((len(disease_idx),))

    for i in sample:
        data[disease_idx[i]] =1
    return data

class call_model(APIView):
    def  get(self,request):
        
        if request.method == 'GET':
            diseaselist = request.GET.getlist('sympbox')
            data = make_data(diseaselist).reshape(1,-1)
            print(data)
            result = AiConfig.model.predict_proba(data)[0]
            out=dict(zip(AiConfig.model.classes_,result))
            sort_orders = sorted(out.items(), key=lambda x: x[1], reverse=True)
            disease=sort_orders[0]

            response = {"predicteddisease":disease[0],
                        'confidencescore':disease[1]}
            print(response)
            return JsonResponse(response)


