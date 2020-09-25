from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse


from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import  diseaseinfo


# Create your views here.


#loading trained_model

import joblib as jb
model = jb.load('models.p')


# Create your views here.
def SearchDisease(request):
    return render(request,'searchdisease.html')


def checkdisease(request):
    import csv
    texts = []
    symptoms=[]
    with open('new.csv', 'r') as csvfile:
        readline=csvfile.readlines()

        for line in readline:
            linesplit=line.split(',')[1]
            if linesplit!='Symptom':
                texts.append(linesplit)
            for one in texts:
                if one not in symptoms:
                    symptoms.append(one)




    csvfile.close()


    disease=[]
    diseaseselect=[]
    with open('new.csv', 'r') as csvdisease:
        readline = csvdisease.readlines()

        for line in readline:
            linesplitdisease = line.split(',')[2]
            if linesplitdisease!='Disease':
                disease.append(linesplitdisease)
            for i in disease:
                if i not in diseaseselect:
                    diseaseselect.append(i)

    csvdisease.close()






    symptomslist = sorted(symptoms)

    alphabaticsymptomslist = sorted(symptomslist)

    if request.method == 'GET':

        return render(request, 'disease/checkdisease.html', {"list2": symptomslist})




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
            print(type(predicted))
            y_pred_2 = model.predict_proba(inputtest)
            confidencescore = y_pred_2.max() * 100
            print(" confidence score of : = {0} ".format(confidencescore))

            confidencescore = format(confidencescore, '.0f')
            predicted_disease = predicted[0]


            # consult_doctor codes----------

            #   doctor_specialization = ["Cardiologist","ENT specialist","Orthopedist","Neurologist",
            #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist and Hepatologist",
            #                            "Dentist","Dietician","General  Physician","Gynaecologist","Hematologist","Lymphologist"
            #                            "Nephrologist","Neurosurgeon","Oncologist","Ophthalmologist",,"Psychiatrist"
            #                            "Speech therapist","Pulmonologist"]
            #
            #
            Allergist_Immunologist = ['Allergy', 'Pneumonia', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue',
                                      'Typhoid']

            Cardiologist = ['Hypertension', 'tricuspid valve insufficiency', 'mitral valve insufficiency',
                            'cardiomyopathy', 'myocardial infarction(heartattack)', 'coronary heart disease',
                            'coronary arteriosclerosis', 'sinus tachycardia ', 'aortic valve stenosis',  'pericardial effusion', 'effusion pericardial', 'Endocarditis', 'congestive heart failure ',
                            'failure heart congestive',  'hypertensive disease']
            Dentist = ['Oralcandidiasis']
            Dermatologist = ['carcinoma', 'cellulitis', 'Exanthema']
            Dietician = ['obesity morbid', 'Obesity']
            ENT_specialist  = ["upper respiratory infection", "deglutition disorder"]
            Gastroenterologist  = ['cirrhosis', 'colitis', 'Diverticulitis',
                                                                 'Diverticulosis', 'Gastritis', 'gastroenteritis',
                                                                 'gastroesophageal reflux disease', 'cirrhosis',
                                                                 'Hepatitis', 'hepatitis B', 'hepatitis C']
            Hepatologist=['cirrhosis', 'colitis', 'Diverticulitis',
                                                                 'Diverticulosis', 'Gastritis', 'gastroenteritis',
                                                                 'gastroesophageal reflux disease', 'cirrhosis',
                                                                 'Hepatitis', 'hepatitis B', 'hepatitis C']
            Physician = ["HIV", "acquired immuno-deficiency syndrome", "Hypoglycemia",
                         "Degenerative polyarthritis", "Diabetes", "Hyperlipidemia", "Hyperglycemia",
                         "Hypercholesterolemia", "Hyperbilirubinemia",  "hiv infections",  "ischemia","ketoacidosis diabetic", "peripheral vascular disease"]
            Gynaecologist = ['fibroid tumor']
            Hematologist = ['anemia', 'Thrombocytopaenia', 'sickle cell anemia', 'Pancytopenia', 'bacteremia']

            Lymphologist = ['lymphatic diseases', 'Lymphoma']
            Nephrologist = ['chronic kidney failure', 'failure kidney', 'insufficiency renal', 'kidney disease',
                             'acute kidney failure ', 'pyelonephritis']
            Neurologist = ["Alzheimer's disease", "accident cerebrovascular" ,"Paranoia","Neuropathy",
                           "Delirium","delusion","dementia","Encephalopathy","Epilepsy","parkinson disease",
                           "Schizophrenia","tonic - clonic epilepsy","transient ischemic attack","tonic - clonic seizures"]

            Neurosurgeon = ["Cerebrovascular accident", "Hemiparesis"]

            Oncologist = ['melanoma', 'adenocarcinoma', 'carcinoma breast', 'carcinoma colon', 'carcinoma of lung', 'carcinoma prostate', 'malignant tumor of colon', 'Malignant\xa0neoplasms', 'Neoplasm', 'primary carcinoma of the liver cells', 'malignant neoplasm of prostate', 'malignant neoplasm of lung', 'malignant neoplasm of breast', 'neoplasm metastasis']
            Ophthalmologist = ['Glaucoma']
            Orthopedist = ['arthritis', 'Osteoporosis']
            Psychiatrist = ["affect labile", "anxiety state", "chronic alcoholic","bipolar disorder", "intoxication(alcoholic intoxication)", "Dependence",
                            "depression mental"," depressive disorder","suicide attempt","confusion", "personality disorder", "psychotic disorder"]

            Speechtherapist = ["aphasia",]

            Pulmonologist = ["Pneumocystis carini  pneumonia", "asthma", "bronchitis","carcinoma of lung", "edema pulmonary", "embolism pulmonary"
                             "emphysema pulmonary",  "chronic obstructive airway disease","hypertension pulmonary", "systemic infection", "spasm bronchial",
                             "Septicemia", "sepsis (invertebrate)", "respiratory failure",  "pneumonia", "aspiration","Paroxysmal dyspnea",  "overload fluid",  "Osteomyelitis",
                             "Neutropenia", "infection", "influenza", "malignant neoplasm of lung"]


            Surgeon = ['adhesion', 'biliary calculus', 'carcinoma colon', 'cholecystitis', 'Hemorrhoids', 'colitis',
                       'malignant tumor of colon', 'deep vein thrombosis', 'Thrombus', 'Hernia', 'Hernia hiatal',
                       'Pancreatitis', 'cholelithiasis', 'decubitus ulcer', 'Pneumothorax']
            Urologist = ['benign prostatic hypertrophy', 'carcinoma prostate', 'malignant neoplasm of prostate',
                         'Incontinence', 'infection urinary tract']

            print('Type of specialist',type(Cardiologist))

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

            elif predicted_disease in Surgeon:
                consultdoctor= "Surgeon"

            elif predicted_disease in Pulmonologist:
                consultdoctor= "Pulmonologist"

            elif predicted_disease in Speechtherapist:
                consultdoctor = "Speechtherapist"

            elif predicted_disease in Psychiatrist:
                consultdoctor = "Psychiatrist"

            elif predicted_disease in Ophthalmologist:
                consultdoctor = "Ophthalmologist"

            elif predicted_disease in Oncologist:
                consultdoctor = "Oncologist"

            elif predicted_disease in Neurosurgeon:
                consultdoctor = "Neurosurgeon"

            elif predicted_disease in Nephrologist:
                consultdoctor = "Nephrologist"

            elif predicted_disease in Lymphologist :
                consultdoctor = "Lymphologist "

            elif predicted_disease in Hematologist:
                consultdoctor = "Hematologist"

            elif predicted_disease in Gynaecologist:
                consultdoctor = "Gynaecologist"

            elif predicted_disease in Physician:
                consultdoctor = "Physician"

            elif predicted_disease in Dietician :
                consultdoctor = "Dietician "

            elif predicted_disease in Hepatologist:
                consultdoctor = "Hepatologist"

            elif predicted_disease in Dentist:
                consultdoctor = "Dentist"

            else:
                consultdoctor = "other"

            # request.session['doctortype'] = consultdoctor

            patientusername=request.user
            user = User.objects.get(username=patientusername)

            # saving to database.....................


            diseasename = predicted_disease
            no_of_symp = inputno
            symptomsname = psymptoms
            confidence = confidencescore

            diseaseinfo_new = diseaseinfo(patient=user, diseasename=diseasename, no_of_symp=no_of_symp,
                                          symptomsname=symptomsname, confidence=confidence, consultdoctor=consultdoctor)
            diseaseinfo_new.save()

            request.session['diseaseinfo_id'] = diseaseinfo_new.id

            print("disease record saved sucessfully.............................")

            a= JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore , "consultdoctor": consultdoctor})
            return render(request,'disease/checkdisease.html',json.loads(a))