import uuid

from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .login import get_user_id_by_token


def get_results(cursor):
    return [dict((cursor.description[i][0], value) \
                              for i, value in enumerate(row)) for row in cursor.fetchall()]


def check_valid_student(token, student_id):
    user = get_user_id_by_token(token)
    query = '''
       SELECT *
       FROM student
       WHERE id=%d AND user_id = %d;
       ''' % (
        student_id,
        user['id']
        )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            fetch_res = [dict((cursor.description[i][0], value) \
                        for i, value in enumerate(row)) for row in cursor.fetchall()]
        except Exception as ex:
            return JsonResponse({}, status=400)
    return fetch_res


@csrf_exempt
def get_student_term_view(request, student_id):
    query = '''
    SELECT *
    FROM student__term JOIN term ON student__term.term_id=term.id
    WHERE student__term.student_id=%d
    ORDER BY term.start_date DESC;
    ''' % (
        student_id,
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            student_terms = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(student_terms, safe=False)


@csrf_exempt
def get_student_section_view(request, student_id, term_id):
    query = '''
    SELECT *
    FROM student__section JOIN section ON student__section.section_id=section.id
    JOIN course ON course.id=section.course_id
    WHERE student_id=%d AND section.term_id=%d;
    ''' % (
        student_id,
        term_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            student_sections = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(student_sections, safe=False)


@csrf_exempt
def create_practice_class_request_view(request, student_id, section_id):
    query = '''
    INSERT INTO practice_class_request (student_id, section_id, status\
                VALUES (%d, %d, %s);
    ''' % (
        student_id,
        section_id,
        "Pending"
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(safe=False)


@csrf_exempt
def get_practice_class_request_view(request, student_id, section_id):
    query = '''
        SELECT * 
        FROM practice_class_request
        WHERE student_id=%d AND section_id=%d;
        ''' % (
        student_id,
        section_id,
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            student_requests = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(student_requests, safe=False)


@csrf_exempt
def get_student_deadlines_view(request, student_id, term_id):
    query = '''
    SELECT course.id as course_id, course.name as course_name, exam.*  
    FROM exam JOIN section ON exam.section_id=section.id JOIN course ON section.course_id=course.id
    WHERE exam.section_id IN     
    (SELECT section_id
    FROM student__section JOIN section ON student__section.section_id=section.id
    WHERE student_id=%d AND term_id =%d);
    ''' % (
        student_id,
        term_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            student_deadlines = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, safe=False, status=400)
    return JsonResponse(student_deadlines, safe=False)
