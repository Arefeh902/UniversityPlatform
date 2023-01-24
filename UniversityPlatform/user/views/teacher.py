from django.http import JsonResponse, Http404
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .login import get_user_id_by_token
import json

def get_results(cursor):
    return [dict((cursor.description[i][0], value) \
                              for i, value in enumerate(row)) for row in cursor.fetchall()]


def check_valid_teacher(token, teacher_id):
    user = get_user_id_by_token(token)
    query = '''
       SELECT *
       FROM teacher
       WHERE id=%d AND user_id = %d;
       ''' % (
        teacher_id,
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
def get_teacher_terms_view(request, teacher_id):
    query = '''
    SELECT * FROM term WHERE id IN
    (SELECT section.term_id FROM teacher__section JOIN section ON teacher__section.section_id=section.id
    WHERE teacher_id=%d)
    ORDER BY term.start_date DESC;
    ''' % (
        teacher_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            teacher_terms = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(teacher_terms, safe=False)


@csrf_exempt
def get_teacher_section_view(request, teacher_id, term_id):
    query = '''
        SELECT section.*, course.name as course_name, course.department, course.credit
        FROM teacher__section JOIN section ON teacher__section.section_id=section.id
        JOIN course ON course.id=section.course_id
        WHERE teacher_id=%d AND section.term_id=%d;
        ''' % (
        teacher_id,
        term_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            teacher_sections = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(teacher_sections, safe=False)


def get_teacher_advisees_view(request, teacher_id):
    query = '''
        SELECT * FROM student 
        JOIN public.user ON public.user.id = student.user_id
        WHERE advisor_id=%d
        ORDER BY sid DESC;
        ''' % (
        teacher_id,
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            students = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(students, safe=False)


@csrf_exempt
def approve_course_registration(request, student_section_id):
    query = '''
            UPDATE student__section 
            SET is_approved=true 
            WHERE id=%s;
            ''' % (
            student_section_id
          )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse({}, safe=False)


@csrf_exempt
def get_teacher_deadlines_view(request, teacher_id, term_id):
    query = '''
    SELECT course.id as course_id, course.name as course_name, exam.*  
    FROM exam JOIN section ON exam.section_id=section.id JOIN course ON section.course_id=course.id
    WHERE exam.section_id IN     
    (SELECT section_id
    FROM teacher__section JOIN section ON teacher__section.section_id=section.id
    WHERE teacher_id=%d AND term_id =%d);
    ''' % (
        teacher_id,
        term_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            student_deadlines = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, safe=False, status=400)
    return JsonResponse(student_deadlines, safe=False)
