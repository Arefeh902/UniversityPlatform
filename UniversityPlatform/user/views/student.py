from django.http import JsonResponse
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
def get_student_detail_view(request, student_id):
    query = '''
        SELECT *
        FROM student JOIN public.user ON student.user_id=public.user.id
        WHERE student.sid=%s
    ''' % (
        student_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            student_detail = get_results(cursor)
        except Exception as ex:
            return JsonResponse({}, status=400)

    return JsonResponse(student_detail, safe=False)


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
    SELECT section.*, course.name as course_name, course.department, course.credit
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
    INSERT INTO practice_class_request (student_id, section_id)
                VALUES (%d, %d);
    ''' % (
        student_id,
        section_id
    )
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except Exception as ex:
            print(ex)
            return JsonResponse({}, status=400)

    return JsonResponse({}, safe=False)


@csrf_exempt
def get_practice_class_request_view(request, student_id, section_id):
    query = '''
        SELECT * 
        FROM practice_class_request
        WHERE student_id=%d AND section_id=%d
        ORDER BY id DESC;
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


@csrf_exempt
def get_student_report_view(request, student_id):
    student_terms_query = '''
    SELECT *
    FROM student__term JOIN term ON student__term.term_id=term.id
    WHERE student__term.student_id=%d
    ORDER BY term.start_date DESC;
    ''' % (
        student_id,
    )

    student_data_query = '''SELECT * FROM student WHERE student.sid=%d''' % (student_id)

    with connection.cursor() as cursor:
        try:
            cursor.execute(student_terms_query)
            student_terms = get_results(cursor)

            cursor.execute(student_data_query)
            student_data = get_results(cursor)[0]
            
            department = student_data.get('department')

            result = []

            for term in student_terms:
                tmp_result = {
                    'term_id': term.get('id'),
                    'term_title': term.get('title'),
                }

                term_id = term.get('id')
                student_report_query = '''SELECT * FROM get_student_courses_report_by_term(%d, %d)''' % (student_id, term_id)
                department_avg_query = '''SELECT * FROM get_department_average('%s', %d);''' % (department, term_id)

                cursor.execute(student_report_query)
                student_reports = get_results(cursor)

                cursor.execute(department_avg_query)
                department_avg_data = get_results(cursor)

                tmp_result['courses'] = student_reports
                tmp_result['department_avg'] = department_avg_data[0].get('avg') if len(department_avg_data) > 0 else ''
                scores = list(map(lambda x: x.get('mark'), student_reports))
                tmp_result['student_avg'] = sum(scores) / len(scores) if len(scores) > 0 else ''

                result.append(tmp_result)


        except Exception as ex:
            return JsonResponse({}, safe=False, status=400)

    return JsonResponse(result, safe=False)


@csrf_exempt
def answer_poll_view(request, student_id):
    pass
