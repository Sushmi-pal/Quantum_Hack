from django.shortcuts import render

from .apps import AiConfig

from django.http import JsonResponse
from rest_framework.views import APIView
from django.conf import settings
from users.models import Doctor
import os
import numpy as np
from django.db.models import Avg, Max, Min
import pandas as pd 
# Create your views here.

def make_data(sample):
    symptoms = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
                'joint_pain',
                'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
                'spotting_ urination',
                'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss',
                'restlessness', 'lethargy',
                'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness',
                'sweating',
                'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite',
                'pain_behind_the_eyes',
                'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
                'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
                'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
                'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
                'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
                'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
                'family_history', 'mucoid_sputum',
                'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
                'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
                'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
                'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
                'yellow_crust_ooze']

    testingsymptoms = []
    # append zero in all coloumn fields...
    for x in range(0, len(symptoms)):
        testingsymptoms.append(0)

        # update 1 where symptoms gets matched...
    for k in range(0, len(symptoms)):

        for z in sample:
            if (z == symptoms[k]):
                testingsymptoms[k] = 1

    inputtest = [testingsymptoms]

    print(inputtest)
    return inputtest


class call_model(APIView):
    consultdoctor=''





    def  get(self,request):
        import csv
        import psycopg2
        from os.path import expanduser

        conn = psycopg2.connect(user="postgres",
                                password="major",
                                host="localhost",
                                port="5432",
                                database="dpsr")

        cursor = conn.cursor()

        cursor.execute("select * from users_doctor;")
        with open("out.csv", "a", newline='') as csv_file:  # Python 3 version
            # with open("out.csv", "wb") as csv_file:              # Python 2 version
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])  # write headers
            csv_writer.writerows(cursor)

        with open("out.csv", "r") as ff:
            reader = csv.reader(ff)
            print('reader', 'reader')
            aa = []
            for row in reader:
                if row not in aa:
                    aa.append(row)
        with open("abc.csv", "w") as fp:
            writer = csv.writer(fp)
            writer.writerows(aa)

        if request.method == 'GET':
            diseaselist = request.GET.getlist('diseaselist')


            data = make_data(diseaselist)
            print(data)
            result = AiConfig.model.predict_proba(data)[0]
            out=dict(zip(AiConfig.model.classes_,result))
            sort_orders = sorted(out.items(), key=lambda x: x[1], reverse=True)
            print('abc',sort_orders)
            disease=sort_orders[0:4]

            ENT_specialist = ["(vertigo) Paroymsal  Positional Vertigo"]

            Physician = ["AIDS", "Chicken pox", "Common Cold", "Dengue", "Diabetes", "Dimorphic hemmorhoids(piles)",
                         "Hypertension ", "Hypoglycemia", "Jaundice", "Malaria", "Typhoid"]

            Dermatologist = ["Acne", "Fungal infection", "Psoriasis", "'Varicose veins’"]

            Allergist_Immunologist = ["Allergy", "Drug Reaction", "Pneumonia", "Tuberculosis"]

            Rheumatologist = ["Arthritis"]

            Pulmonologist = ["Bronchial Asthma"]
            Gynaecologist = ["Cervical spondylosis"]
            Gastroenterologist = ["Dimorphic hemmorhoids(piles)", "GERD", "Gastroenteritis", "Hepatitis B", "Hepatitis C",
                                  "Hepatitis D", "Hepatitis E", "Peptic ulcer disease", "hepatitis A",
                                  "Chronic cholestasis"]
            Cardiologist = ["Heart attack"]
            Endocrinologist = ["Hyperthyroidism", "Hypothyroidism"]
            Orthopedist = ["Impetigo", "Osteoarthristis"]
            Neurologist = ["Migraine", "Paralysis (brain hemorrhage)"]
            Nephrologist = ["Urinary tract infection"]
            Hematologist = ["Alcoholic hepatitis"]

            print('Type of specialist', type(Cardiologist))
            print("Allergy" in Allergist_Immunologist)
            print(type(str(disease[0][0])))
            print(disease[0][0])
            if str(disease[0][0]) in Cardiologist:

                consultdoctor = "Cardiologist"



            elif str(disease[0][0]) in ENT_specialist:

                consultdoctor = "ENT"

            elif str(disease[0][0]) in Orthopedist:

                consultdoctor = "Orthopedist"

            elif str(disease[0][0]) in Neurologist:

                consultdoctor = "Neurologist"

            elif str(disease[0][0]) in Allergist_Immunologist:


                consultdoctor = "Allergist"



            elif str(disease[0][0]) in Dermatologist:

                consultdoctor = "Dermatologist"

            elif str(disease[0][0]) in Gastroenterologist:

                consultdoctor = "Gastroenterologist"

            elif str(disease[0][0]) in Endocrinologist:

                consultdoctor = "Endocrinologist"

            elif str(disease[0][0]) in Pulmonologist:

                consultdoctor = "Pulmonologist"

            elif str(disease[0][0]) in Rheumatologist:

                consultdoctor = "Rheumatologist"


            elif str(disease[0][0]) in Nephrologist:

                consultdoctor = "Nephrologist"


            elif str(disease[0][0]) in Hematologist:

                consultdoctor = "Hematologist"

            elif str(disease[0][0]) in Gynaecologist:

                consultdoctor = "Gynaecologist"

            elif str(disease[0][0]) in Physician:

                consultdoctor = "Physician"



            else:

                consultdoctor = "General Physician"

            predicted_disease = []
            predicted_score = []
            for i in disease:
                predicted_disease.append(i[0])
                predicted_score.append(i[1])

            print(predicted_score)

            response = {"Prediction":predicted_disease,
                        'Probab':predicted_score,
                        'Consult':consultdoctor}

            doctorr=Doctor.objects.filter(speciality__icontains=consultdoctor)
            print(doctorr)
            highest_experience = doctorr.aggregate(Max('experience_yrs'))
            print('experience',highest_experience)
            lowest_fee=Doctor.objects.filter(speciality__icontains=consultdoctor,experience_yrs=highest_experience['experience_yrs__max'])
            print('low',lowest_fee)
            resultt=lowest_fee.aggregate(Min('fee'))
            print('final',resultt)
            r=Doctor.objects.filter(speciality__icontains=consultdoctor,experience_yrs=highest_experience['experience_yrs__max'],fee=resultt['fee__min'])
            print('result',r)
            print(response)
            return JsonResponse(response)

# def consult(request):
#     query = request.GET['resultSpecialist']
#     print(query)
#     if len(query) > 85:
#         speciality = []
#     else:
#         Sname = doctor_profile.objects.filter(name__icontains=query)
#         Sdesc = doctor_profile.objects.filter(desc__icontains=query)
#         speciality = Sname.union(Sdesc)
#     if speciality.count() == 0:
#         messages.error(request, 'No Search result found. Please refine your query')
#
#     params = {'speciality': speciality, 'query': query}
#     return render(request, 'search.html', params)


