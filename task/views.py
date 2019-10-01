from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Rules
from django.utils import six
import json

from pythonds.basic.stack import Stack
from pythonds.trees.binaryTree import BinaryTree


def home(request):
    return render(request, 'base.html', {})


"""
В template/MyRule1.json представлена структура правила.
 
(systolic_bp > 140 and abdominal_pain = true) or diastolic_bp < 90

MyRule2.json
(systolic_bp > 140 and abdominal_pain) or (age > 21 and gender = "female")
"""


@csrf_exempt
def json_message(request):
    result = []
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        for i in Rules.objects.all():
            rule = i.rule

            answer = unary_operator(rule, data)
            if answer:
                result.append(rule["result"])

            answer = binary_operator_and(rule, data)
            if answer:
                result.append(rule["result"])

            answer = binary_operator_or(rule, data)
            if answer:
                result.append(rule["result"])

    return JsonResponse(json.dumps(result), safe=False)


def unary_operator(rule, data):
    if rule["relation"] is None:
        if rule['code'] in data:

            if rule["operator"] == "=":
                if data[rule["code"]] == rule["compared"]:
                    return True

            if rule["operator"] == ">":
                if data[rule["code"]] > rule["compared"]:
                    return True

            if rule["operator"] == "<":
                if data[rule["code"]] < rule["compared"]:
                    return True
            return False
    return False


def binary_operator_and(rule, data):
    if rule["relation"] == 'and':

        check = 0
        for condition in rule['conditions']:
            answer = unary_operator(condition, data)
            if answer:
                check += 1
            answer = binary_operator_and(condition, data)
            if answer:
                check += 1
            answer = binary_operator_or(condition, data)
            if answer:
                check += 1
        if check == len(rule['conditions']):
            return True
    return False


def binary_operator_or(rule, data):
    if rule["relation"] == 'or':

        check = 0
        for condition in rule['conditions']:
            answer = unary_operator(condition, data)
            if answer:
                check += 1
            answer = binary_operator_and(condition, data)
            if answer:
                check += 1
            answer = binary_operator_or(condition, data)
            if answer:
                check += 1
        if check > 0:
            return True
    return False
