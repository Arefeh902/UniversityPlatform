from django.urls import path
from .views.login import login_view
from .views.student import *
from .views.section import *
from .views.teacher import *
from .views.course_registration import *


urlpatterns = [
   path('user/login/', login_view, name='login'),

   path('student/<int:student_id>/terms/', get_student_term_view, name='student_terms'),
   path('student/<int:student_id>/detail/', get_student_detail_view),
   path('student/<int:student_id>/section/<int:term_id>/', get_student_section_view, name='student_term_section'),
   path('student/<int:student_id>/practice-class-request/create/<int:section_id>/', create_practice_class_request_view),
   path('student/<int:student_id>/practice-class-request/<int:section_id>/', get_practice_class_request_view),
   path('student/<int:student_id>/deadline/<int:term_id>/', get_student_deadlines_view),
   path('student/<int:student_id>/report/', get_student_report_view),
   path('student/<int:student_id>/course-registration/<int:term_id>/<str:department>/',
        get_student_course_registration_in_department_sections),
   path('student/<int:student_id>/course-registration/select-section/<int:section_id>/', select_section),
   path('student/<int:student_id>/course-registration/delete-section/<int:section_id>/', delete_section),


   path('teacher/<int:teacher_id>/terms/', get_teacher_terms_view),
   path('teacher/<int:teacher_id>/section/<int:term_id>/', get_teacher_section_view),
   path('teacher/<int:teacher_id>/get-students/', get_teacher_advisees_view),
   path('teacher/<int:teacher_id>/deadline/<int:term_id>/', get_teacher_deadlines_view),


   path('section/<int:section_id>/detail/', get_section_detail_view),
   path('section/<int:section_id>/practice-class-request/all/', get_section_practice_class_request_view),
   path('section/<int:section_id>/practice-class-request/<int:request_id>/set-status/',
        set_practice_class_request_status_view),
   path('section/<int:section_id>/students/', get_section_students_view),
   path('section/<int:section_id>/create-exam-poll/', create_exam_poll_view),
   path('section/<int:term_id>/<str:department>/all', get_all_sections_of_departments_in_term),


   path('department/all', get_all_departments),
   path('department/<str:department>/term/<int:term_id>/average/', get_department_average),
   path('department/<str:department>/chart', get_department_chart_view),
]
