# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import nltk

# Create your views here.

from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import requests
import pandas as pd
# Create your views here.
@api_view(["POST"])
def answer(msgdata):
    try:
        print(str(msgdata))
        # print(msgdata.POST['message'])
        # print(type(msgdata.body))
        # message_text=json.loads(msgdata.body)

        lines=msgdata.POST['message']
        sentences = nltk.sent_tokenize(lines) #tokenize sentences
        nouns = [] #empty to array to hold all nouns

        for sentence in sentences:
            for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
                if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                    nouns.append(word)

        string = ' '.join(nouns)
        print(" the string being sent for api call is "+str(string))
        response = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/cd814...xxx ...446.... xxxxx.... c13c7a9?subscription-key=42cd... xxx ....024cbd957xxxxx082a0c&q='+string)
        data = pd.read_csv('/home/ghw/tutorial/risetocode/Harvey/Chatbot/data3.csv',encoding="utf-8", sep=',', index_col=False)
        df = pd.DataFrame(data)

        luis_response=response.json()  
        list_entities=luis_response["entities"]
        answer_description="Short Answer"
        domainNotAssigned=1
        intentNotAssigned=1
        locationNotAssigned=1
        location="Alabama"
        for single_entity in list_entities:
            if single_entity["type"]=="geog_type":
                location=single_entity["resolution"]["values"][0]
                locationNotAssigned=0
            if single_entity["type"]=="domain_type":
                answer_description=single_entity["resolution"]["values"][0]
                domainNotAssigned=0
            if single_entity["type"]=="intent_type":
                question=single_entity["resolution"]["values"][0]
                intentNotAssigned=0

        if(intentNotAssigned==1):
            rstr="Sorry. I did not get you"
            return JsonResponse(rstr,safe=False)
        if(locationNotAssigned==1 and domainNotAssigned==1):
            rstr="Please provide the jurisdiction area and question description"
            return JsonResponse(rstr,safe=False)
        if(locationNotAssigned==1):
            rstr="Please provide the jurisdiction area"
            return JsonResponse(rstr,safe=False)
        if(domainNotAssigned==1):
            d2 = df[(df['Question']==question) & (df['AnswerDescription']=="Short Answer") & (df['State']==location)]      
            domain_extra=(d2.iloc[0]['Answer'])
            return JsonResponse("Uhh.. I need more details on the question to come up with an accurate answer. Here is what I came up with: "+domain_extra,safe=False)

        print("got location as "+location+" got answer description as "+answer_description+" question as "+question)
        d2 = df[(df['Question']==question) & (df['AnswerDescription']==answer_description) & (df['State']==location)]      
        return JsonResponse(str(d2.iloc[0]['Answer']),safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)


