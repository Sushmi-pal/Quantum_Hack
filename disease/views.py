from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse


from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import  diseaseinfo


# Create your views here.


#loading trained_model




# Create your views here.
def SearchDisease(request):
    return render(request,'searchdisease.html')


def checkdisease(request):
    import csv
    texts = []
    symptoms=[]
    with open('symptoms.csv', 'r') as csvfile:
        readline=csvfile.readlines()
        for line in readline:
            texts.append(line.split(',"')[0])
        for i in texts:
            symptoms.append(i[1:-1])


    diseaselist = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer diseae',
                   'AIDS', 'Diabetes ',
                   'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'Cervical spondylosis',
                   'Paralysis (brain hemorrhage)',
                   'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B',
                   'Hepatitis C', 'Hepatitis D',
                   'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
                   'Dimorphic hemmorhoids(piles)',
                   'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
                   'Osteoarthristis',
                   'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection',
                   'Psoriasis', 'Impetigo']

    symptomslist = sorted(symptoms)

    alphabaticsymptomslist = sorted(symptomslist)

    if request.method == 'GET':

        return render(request, 'disease/checkdisease.html', {"list2": alphabaticsymptomslist})




    elif request.method == 'POST':

        ## access you data by playing around with the request.POST object

        inputno = int(request.POST["noofsym"])
        print(inputno)
        if (inputno == 0):
            return JsonResponse({'predicteddisease': "none", 'confidencescore': 0})

        else:

            psymptoms = []
            psymptoms = request.POST.getlist("symptoms[]")

            print(psymptoms)

            """      #main code start from here...
            """

            testingsymptoms = []
            # append zero in all coloumn fields...
            for x in range(0, len(symptomslist)):
                testingsymptoms.append(0)

            # update 1 where symptoms gets matched...
            for k in range(0, len(symptomslist)):

                for z in psymptoms:
                    if (z == symptomslist[k]):
                        testingsymptoms[k] = 1

            inputtest = [testingsymptoms]

            print(inputtest)

            predicted = model.predict(inputtest)
            print("predicted disease is : ")
            print(predicted)

            y_pred_2 = model.predict_proba(inputtest)
            confidencescore = y_pred_2.max() * 100
            print(" confidence score of : = {0} ".format(confidencescore))

            confidencescore = format(confidencescore, '.0f')
            predicted_disease = predicted[0]

            # consult_doctor codes----------

            #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
            #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]

            Rheumatologist = ['Osteoarthristis', 'Arthritis']

            Cardiologist = ['Heart attack', 'Bronchial Asthma', 'Hypertension ']

            ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo', 'Hypothyroidism']

            Orthopedist = []

            Neurologist = ['Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis']

            Allergist_Immunologist = ['Allergy', 'Pneumonia',
                                      'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid']

            Urologist = ['Urinary tract infection',
                         'Dimorphic hemmorhoids(piles)']

            Dermatologist = ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo']

            Gastroenterologist = ['Peptic ulcer diseae', 'GERD', 'Chronic cholestasis', 'Drug Reaction',
                                  'Gastroenteritis', 'Hepatitis E',
                                  'Alcoholic hepatitis', 'Jaundice', 'hepatitis A',
                                  'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Diabetes ', 'Hypoglycemia']

            if predicted_disease in Rheumatologist:
                consultdoctor = "Rheumatologist"

            if predicted_disease in Cardiologist:
                consultdoctor = "Cardiologist"


            elif predicted_disease in ENT_specialist:
                consultdoctor = "ENT specialist"

            elif predicted_disease in Orthopedist:
                consultdoctor = "Orthopedist"

            elif predicted_disease in Neurologist:
                consultdoctor = "Neurologist"

            elif predicted_disease in Allergist_Immunologist:
                consultdoctor = "Allergist/Immunologist"

            elif predicted_disease in Urologist:
                consultdoctor = "Urologist"

            elif predicted_disease in Dermatologist:
                consultdoctor = "Dermatologist"

            elif predicted_disease in Gastroenterologist:
                consultdoctor = "Gastroenterologist"

            else:
                consultdoctor = "other"

            request.session['doctortype'] = consultdoctor

            patientusername = request.session['patientusername']
            puser = User.objects.get(username=patientusername)

            # saving to database.....................

            patient = puser.patient
            diseasename = predicted_disease
            no_of_symp = inputno
            symptomsname = psymptoms
            confidence = confidencescore

            diseaseinfo_new = diseaseinfo(patient=patient, diseasename=diseasename, no_of_symp=no_of_symp,
                                          symptomsname=symptomsname, confidence=confidence, consultdoctor=consultdoctor)
            diseaseinfo_new.save()

            request.session['diseaseinfo_id'] = diseaseinfo_new.id

            print("disease record saved sucessfully.............................")

            return JsonResponse({'predicteddisease': predicted_disease, 'confidencescore': confidencescore,
                                 "consultdoctor": consultdoctor})

