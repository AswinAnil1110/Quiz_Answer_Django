from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from json import loads

# Create your views here.
questions = [
    {
        "id": 1,
        "question": "Which language is used with Django?",
        "options": ["Java", "Python", "C++", "PHP"],
        "answer": "Python",
        "marks": 5
    },
    {
        "id": 2,
        "question": "Which datatype stores data in key-value pairs?",
        "options": ["List","Set","Tuple","Dictionary"],
        "answer": "Dictionary",
        "marks": 5
    },
    {
        "id": 3,
        "question": "Which HTTP method is commonly used to retrieve data?",
        "options": ["POST", "GET", "DELETE", "PUT"],
        "answer": "GET",
        "marks": 5
    }]

class QuizQuestionView(View):
    def get(self,request):
        data = []
        for question in questions:
            question_data = {
                            "id": question.get("id"),
                            "question": question.get("question"),
                            "options": question.get("options"),
                            "marks": question.get("marks")
                            }
            data.append(question_data)
        return JsonResponse(data,safe=False)
    
@method_decorator(csrf_exempt,name='dispatch')
class CheckAnswerView(View):
    def post(self,request):
        request_body = request.body
        form_data = loads(request_body)
        question_id = form_data.get('question_id')
        submitted_answer = form_data.get('answer')
        question_data = None

        for question in questions:
            if question.get('id') == question_id:
                question_data = question
                break
        
        if question_data is None:
            return JsonResponse({"Message":"No Question Exists"})
        
        if submitted_answer == question_data.get('answer'):
            result = (
                        {
                            "question_id": question_id,
                            "correct": True,
                            "marks_obtained": question_data.get("marks"),
                            "message": "Correct answer!"
                        })
        else:
            result = (
                        {
                            "question_id": question_id,
                            "correct": False,
                            "marks_obtained": 0,
                            "message": "Wrong answer!"
                        })
        
        return JsonResponse(result)

@method_decorator(csrf_exempt,name='dispatch')
class QuizResultView(View):
    def post(self,request):
        request_body = request.body
        form_data = loads(request_body)
        submitted_answer = form_data.get('answers',[])
        total_marks = 0
        obtained_marks = 0
        results = []

        for data in submitted_answer:
            question_id = data.get('question_id')
            answer = data.get('answer')

            for question in questions:
                if question.get('id') == question_id:
                    total_marks += question.get('marks')
                    if answer == question.get('answer'):
                        obtained_marks += question.get('marks')
                        status = 'Correct'
                    else:
                        status = 'Wrong'
                    result = {
                                "question_id": question_id,
                                "submitted_answer": answer,
                                "status": status
                             }
                    results.append(result)
                    break
        data = {
                    "total_marks": total_marks,
                    "obtained_marks": obtained_marks,
                    "result": results
               }
        return JsonResponse(data)