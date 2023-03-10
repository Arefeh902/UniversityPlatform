import json

from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


def get_results(cursor):
    return [dict((cursor.description[i][0], value) \
                              for i, value in enumerate(row)) for row in cursor.fetchall()]


@csrf_exempt
def get_section_detail_view(request, section_id):
    query = '''
    SELECT *
    FROM section
    WHERE id=%d;
    ''' % (
        section_id,
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            section_detail = get_results(cursor)[0]
        except Exception as ex:
            return JsonResponse({}, status=400)
    query = '''
    SELECT *
    FROM course
    WHERE id=%d;
    ''' % (
        section_detail['course_id'],
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            course_detail = get_results(cursor)[0]
        except Exception as ex:
            return JsonResponse({}, status=400)
    query = '''
    SELECT teacher.id AS id, public.user.first_name, public.user.last_name
    FROM teacher__section JOIN teacher ON teacher__section.teacher_id=teacher.id
    JOIN public.user ON public.user.id=teacher.user_id
    WHERE section_id=%d;
    ''' % (
        section_id,
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            teachers = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)
    query = '''
    SELECT *
    FROM section_time
    WHERE section_id=%d;
    ''' % (
        section_id,
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            times = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    response_data = section_detail
    response_data['course'] = course_detail
    response_data['teachers'] = teachers
    response_data['times'] = times
    return JsonResponse(response_data, safe=False)


@csrf_exempt
def get_section_students_view(request, section_id):
    query = '''
            SELECT * 
            FROM student__section JOIN student ON student__section.student_id=student.sid
            JOIN public.user ON student.user_id = public.user.id
            WHERE section_id=%d
            ''' % (
        section_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            students = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(students, safe=False)


@csrf_exempt
def get_section_practice_class_request_view(request, section_id):
    query = '''
        SELECT * 
        FROM practice_class_request JOIN student ON practice_class_request.student_id=student.sid
        WHERE practice_class_request.section_id=%d
        ORDER BY practice_class_request.id DESC;
        ''' % (
        section_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            students = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(students, safe=False)


@csrf_exempt
def set_practice_class_request_status_view(request, section_id, request_id):
    data = json.loads(request.body)
    query = '''
        UPDATE practice_class_request 
        SET status='%s' WHERE id=%d;
        ''' % (
        data.get('status'),
        request_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse({}, safe=False)


@csrf_exempt
def create_exam_poll_view(request, section_id):
    data = json.loads(request.body)
    query = '''
        INSERT INTO exam_poll 
        (start_at, end_at, section_id, type, title) 
        VALUES (%s, %s, %s, %s, %s)
        ''' % (
            data.get('start_at'),
            data.get('end_at'),
            section_id,
            data.get('type'),
            data.get('title')
        )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse({}, safe=False)


@csrf_exempt
def add_poll_option(request, exam_poll_id):
    pass


@csrf_exempt
def get_all_section_exam_polls(request, section_id):
    pass
