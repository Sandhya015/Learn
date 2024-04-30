from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Category, Question
import logging

logger = logging.getLogger(__name__)

def home(request):
    try:
        categories = Category.objects.all()
        context = {'categories': categories}
        if request.GET.get('category'):
            category_name = request.GET.get('category')
            return redirect(f"/quiz/?category={category_name}")
        return render(request, 'home.html', context)
    except Exception as e:
        logger.error(f"An error occurred in home view: {e}")
        return HttpResponse("Something went wrong")

def quiz(request):
    try:
        category_name = request.GET.get('category')
        if not category_name:
            return HttpResponse("Category not provided")

        questions = Question.objects.filter(category__category_name__iexact=category_name)

        context = {'category_name': category_name, 'questions': questions}
        return render(request, 'quiz.html', context)

    except Exception as e:
        logger.error(f"An error occurred in quiz view: {e}")
        return HttpResponse("Something went wrong")

def get_quiz(request):
    try:
        category_name = request.GET.get('category')
        if not category_name:
            return JsonResponse({'status': False, 'message': 'Category not provided'})
        
        # Filter questions based on the category provided
        questions = Question.objects.filter(category__category_name__iexact=category_name)
        
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
