from django.urls import path
from .views.login import login_view
from .views.student import *
from .views.section import *
from .views.teacher import *

urlpatterns = [
   path('login/', login_view, name='login'),

   path('student/<int:student_id>/terms/', get_student_term_view, name='student_terms'),
   path('student/<int:student_id>/section/<int:term_id>/', get_student_section_view, name='student_term_section'),
   path('student/<int:student_id>/practice-class-request/create/<int:section_id>/', create_practice_class_request_view),
   path('student/<int:student_id>/practice-class-request/<int:section_id>/', get_practice_class_request_view),
   path('student/<int:student_id>/deadline/<int:term_id>/', get_student_deadlines_view),

   path('teacher/<int:teacher_id>/terms/', get_teacher_terms_view),
   path('teacher/<int:teacher_id>/section/<int:term_id>/', get_teacher_section_view),
   path('teacher/<int:teacher_id>/get-students/', get_teacher_advisees_view),

   path('section/<int:section_id>/detail/', get_section_detail_view),
   path('section/<int:section_id>/practice-class-request/all/', get_section_practice_class_request_view),
   path('section/<int:section_id>/practice-class-request/set-status/', set_practice_class_request_status_view),
   path('section/<int:section_id>/students/', get_section_students)

]
