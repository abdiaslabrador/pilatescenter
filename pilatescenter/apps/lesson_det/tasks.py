from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from apps.exercise.models import Exercise

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

@task(name="comida")
def anoter(name='task_prueba'):
	h = Exercise.objects.create(name= name)
	h.save()
