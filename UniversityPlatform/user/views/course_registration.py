from django.http import JsonResponse, Http404
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


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


@csrf_exempt
def get_student_course_registration_in_department_sections(request, student_id, term_id, department):
    query = '''SELECT * FROM get_student_course_registration_sections(%d, %d, '%s');''' % (student_id, term_id, department)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            sections = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(sections, safe=False)


@csrf_exempt
def select_section(request, student_id, section_id):
    query = '''
            INSERT INTO 
            student__section (student_id, section_id)
            VALUES (%d, %d);
            ''' % (
        student_id,
        section_id,
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            result = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=500)
    if len(result) == 0:
        return JsonResponse({}, status=400)
    return JsonResponse({}, safe=False)


@csrf_exempt
def delete_section(request, student_section_id):
    query = '''
              DELETE
              FROM student__section 
              WHERE id=%d;
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
def get_department_average(request, department, term_id):
    query = '''SELECT * FROM get_department_average(%s, %d);''' % (department, term_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            department_average = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(department_average, safe=False)


@csrf_exempt
def get_department_chart_view(request, department):
    query = '''SELECT * FROM get_chart('%s');''' % (department)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            chart = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(chart, safe=False)
