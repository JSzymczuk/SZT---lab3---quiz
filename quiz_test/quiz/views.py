from django.shortcuts import render
from mongoengine import *
from django.http import HttpResponse
from .models import Answer, Question, Attempt, AnsweredQuestion


def index(request):
	return render(request, 'index.html', {})
	
	
def questions(request):
	connect('quiz')
	context = {
		'questions': Question.objects,
		'count': Question.objects.count()
	}
	return render(request, 'questions.html', context)
	
	
def topscores(request):
	connect('quiz')
	
	return render(request, 'top-scores.html', { 'scores': Attempt.objects[:10] })
	
	
def loader(request):
	return render(request, 'loader.html', {})

	
def score(request):
	connect('quiz')
	result = Attempt(username = request.POST.get('username', ''), score = 0)
	
	for q in Question.objects:
		qid = str(q.id);
		ans = request.POST.getlist('question[' + qid + ']')
		result.answers.append(AnsweredQuestion(question_id = qid, answers = ans))
		if q.type == 0:
			if len(ans) == 1 and ans[0] == str(next(a for a in q.answers if a.is_correct)._id):
				result.score += q.points
		elif q.type == 1 and len(q.answers) > 0:
			correct = 0
			for a in q.answers:
				if (a.is_correct and str(a._id) in ans) or (not a.is_correct and str(a._id) not in ans):
					correct += 1
			result.score += correct * q.points / len(q.answers)
		elif q.type == 2:
			if len(ans) == 1 and any(a.text.lower() == ans[0].lower() for a in q.answers):
				result.score += q.points
		elif q.type == 3:
			if len(ans) == 1 and any(a.text == ans[0] for a in q.answers):
				result.score += q.points
			
	result.save()
	return render(request, 'score.html', { 'score': result.score })
