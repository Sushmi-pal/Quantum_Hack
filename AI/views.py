from django.shortcuts import render

from .apps import AiConfig

from django.http import JsonResponse
from rest_framework.views import APIView

import pandas as pd 
# Create your views here.

def make_data(sample):
    X = pd.read_csv("models/data/all_x.csv")
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
            diseaselist = request.GET.get('diseaselist')
            data = make_data(diseaselist).reshape(1,-1)

            result = AiConfig.model.predict_proba(data)[0]
            out=dict(zip(model.classes_,result))
            sort_orders = sorted(out.items(), key=lambda x: x[1], reverse=True)
            disease=sort_orders[0]

            response = {"Prediction":disease[0],
                        'Probab':disease[1]}

            return JsonResponse(response)


