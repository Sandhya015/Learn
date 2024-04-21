from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  # Import JsonResponse
from .models import *
import random

# Create your views here.
def home(request):
    return HttpResponse("Hello world")

def get_quiz(request):
    try:
        question_objs = Question.objects.all()
        data = []
        

        for question_obj in question_objs:
            print(question_obj.get_answers())
            data.append({
                "category": question_obj.category.category_name,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answers":question_obj.get_answers()

            })
        
        payload = {'status': True, 'data': data}  # Added comma after 'status': True

        return JsonResponse(payload)
    
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")
