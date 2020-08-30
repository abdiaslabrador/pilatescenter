from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from apps.exercise.models import Exercise
from apps.lesson_det.models import Lesson_det
from datetime import datetime

@task(name="sum_two_numbers")
def add(x, y):
    return x + y

@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)

@task(name="saludo")
def print_name():
	print("HOLA")

@task(name="lessons")
def run_lesson():

	today = datetime.today()
	lessons = Lesson_det.objects.filter(
								reset= False,
								day_lesson= today.date()
							)

	if lessons:
		for lesson in lessons:
			# print(lesson.hour_chance.hour == today.hour and lesson.hour_chance.minute == today.minute)
			if lesson.hour_chance.hour == today.hour and lesson.hour_chance.minute == today.minute:
				lesson.lesson_status = lesson.NOTCHANCE
				lesson.save()
			elif lesson.hour_lesson.hour == today.hour and lesson.hour_lesson.minute == today.minute:
				lesson.lesson_status = lesson.INPROCESS
				lesson.save()
			elif lesson.hour_end.hour == today.hour and lesson.hour_end.minute == today.minute:
				lesson.lesson_status = lesson.FINISHED
				lesson.save()
	else:
		print("No hay lecciones")