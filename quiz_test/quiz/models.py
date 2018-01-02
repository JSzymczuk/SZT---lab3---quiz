from django.db import models
from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, IntField, FloatField, BooleanField, ListField, EmbeddedDocumentField, ObjectIdField
from bson.objectid import ObjectId
from enum import Enum


class Test(Document):
	name = StringField(required=True)
	meta = { 
		'collection': 'test' 
	}

	
class Answer(EmbeddedDocument):
	_id        = ObjectIdField(required=True, default=lambda:ObjectId())
	text       = StringField(max_length=200)
	order      = IntField(default=0)
	is_correct = BooleanField(default=False)
	
	meta = {
		'ordering':         ['order']
	}
	
	def __str__(self):
		return self.text
		
	def __cmp__(self, other):
		if hasattr(other, 'order'):
			return self.order.__cmp__(other.order)
			
	def get_id(self): 
		return getattr(self, '_id', '') 

			
class Question(Document):
	SingleChoice   = 0
	MultipleChoice = 1
	TextInput      = 2
	NumberInput    = 3
	
	Choices = (
		(SingleChoice,   'Jednokrotnego wyboru'),
		(MultipleChoice, 'Wielokrotnego wyboru'),
		(TextInput,      'Otwarte tekstowe'),
		(NumberInput,    'Otwarte liczbowe')
	)
	
	text      = StringField(max_length = 200)
	points    = IntField(default = 1)
	order     = IntField(default = 0)
	type      = IntField(choices = Choices, default = SingleChoice)
	answers   = ListField(EmbeddedDocumentField(Answer))
	
	meta = { 
		'collection':       'questions',		
		'ordering':         ['order']
	}
	
	def __str__(self):
		return self.text
		
	def __cmp__(self, other):
		if hasattr(other, 'order'):
			return self.order.__cmp__(other.order)

			
class AnsweredQuestion(EmbeddedDocument):
	question_id = StringField()
	answers     = ListField(StringField())
			
			
class Attempt(Document):
	username = StringField()
	score    = FloatField()
	answers  = ListField(EmbeddedDocumentField(AnsweredQuestion))
	
	meta = { 
		'collection':       'attempts',		
		'ordering':         ['-score']
	}
				
#class NumericQuestion(Question):
#	tolerance = FloatField(default = 0)
	