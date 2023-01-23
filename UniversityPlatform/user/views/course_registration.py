from django.http import JsonResponse, Http404
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json


def get_results(cursor):
    return [dict((cursor.description[i][0], value) \
                              for i, value in enumerate(row)) for row in cursor.fetchall()]


@csrf_exempt
def get_all_departments(request):
    query = '''
           SELECT * FROM department;
           '''
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            departments = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(departments, safe=False)


@csrf_exempt
def get_all_sections_of_departments_in_term(request, term_id, department):
    query = '''
           SELECT * 
           FROM section JOIN course ON section.course_id=course.id
           WHERE section.term_id=%d AND course.department=%s;
           ''' % (
            term_id,
            department,
            )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            sections = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(sections, safe=False)

