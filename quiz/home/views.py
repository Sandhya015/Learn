from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse  
from .models import Category, Question  
import logging  

logger = logging.getLogger(__name__)


def home(request):
    try:
        categories = Category.objects.all()
        context = {'categories': categories}
        if request.GET.get('category'):  # Fixing the syntax for accessing GET parameters
            return redirect(f"/quiz/?category={request.GET.get('category')}")  # Fixing the syntax for accessing GET parameters
        return render(request, 'home.html', context)
    except Exception as e:
        logger.error(f"An error occurred in home view: {e}")
        return HttpResponse("Something went wrong")
    
def quiz(request):
    return render(request,'quiz.html')
def get_quiz(request):
    try:
        # Fetch all questions and their answers
        questions = Question.objects.all()
        data = []
        for question in questions:
            data.append({
                "category": question.category.category_name,
                "question": question.question,
                "marks": question.marks,
                "answers": question.get_answers()
            })
        
        payload = {'status': True, 'data': data}  
        return JsonResponse(payload)
    
    except Exception as e:
        logger.error(f"An error occurred in get_quiz view: {e}")
        return HttpResponse("Something went wrong")
