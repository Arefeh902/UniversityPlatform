from django.urls import path
from .views.login import login_view
from .views.student import *
urlpatterns = [
   path('login/', login_view, name='login'),
   path('student/<int:student_id>/terms/', get_student_term_view, name='student_terms'),
   path('student/<int:student_id>/section/<int:term_id>/', get_student_section_view, name='student_term_section'),
   path('student/<int:student_id>/practice-class-request/create/<int:section_id>', create_practice_exam_request_view),
]