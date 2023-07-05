from django.views import generic
from .models import Course


class CourseList(generic.ListView):
    model = Course
    queryset = Course.objects.all()
    template_name = 'course_list.html'
