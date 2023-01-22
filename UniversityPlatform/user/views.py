import uuid

from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


def get_user_id_by_token(req_meta):
    if not 'HTTP_AUTHORIZATION' in req_meta:
        return None
    token = req_meta['HTTP_AUTHORIZATION']
    query = '''
    SELECT *
    FROM public.user
    WHERE token=%s;
    ''' % (
        token
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = [dict((cursor.description[i][0], value) \
                              for i, value in enumerate(row)) for row in cursor.fetchall()][0]
        except Exception as ex:
            print(str(ex))
            return None
    if fetch_res:
        return fetch_res
    return None


def get_user_student_infos(user_id: int):
    query = '''
       SELECT *
       FROM student
       WHERE user_id = %d;
       ''' % (
        user_id
        )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = [dict((cursor.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cursor.fetchall()]
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                 json_dumps_params={'ensure_ascii': False})
    return fetch_res


def get_user_teacher_infos(user_id: int):
    query = '''
       SELECT *
       FROM teacher
       WHERE user_id=%d;
       ''' % (
        user_id
        )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = [dict((cursor.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cursor.fetchall()]
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                 json_dumps_params={'ensure_ascii': False})
    return fetch_res


def get_user_employee_infos(user_id: int):
    query = '''
       SELECT *
       FROM employee
       WHERE user_id=%d;
       ''' % (
        user_id
        )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = [dict((cursor.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cursor.fetchall()]
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                 json_dumps_params={'ensure_ascii': False})
    return fetch_res


@csrf_exempt
def login_view(request):
    print(request.POST)
    query = '''
    SELECT *
    FROM public.user
    WHERE username='%s' AND password='%s';
    ''' % (
        request.POST. get('username'),
        request.POST.get('password'),
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            user = [dict((cursor.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cursor.fetchall()][0]
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
    user_id = user['id']
    print(user_id)
    token = uuid.uuid4()
    query = '''
        UPDATE public.user
        SET token='%s';
        ''' % (
        token
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except Exception as ex:
            return JsonResponse({'result': False, 'errors': [str(ex)]}, safe=False,
                                json_dumps_params={'ensure_ascii': False})
    response_data = user
    response_data['token'] = token
    response_data['student_infos'] = get_user_student_infos(user_id)
    response_data['teacher_infos'] = get_user_teacher_infos(user_id)
    response_data['employee_infos'] = get_user_employee_infos(user_id)
    print(response_data)
    return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

