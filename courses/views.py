from rest_framework import generics, permissions
from .models import  TermCourse
from .serializers import  TermCourseSerializer
from academics.models import Semester
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsCourseInstructor, IsCourseStudent, IsCourseStaff

class CourseListView(generics.ListAPIView):
    serializer_class = TermCourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'course__department', 'course__is_core', 'semester', 'instructor', 'is_active',]
    search_fields = ['course']

    def get_queryset(self):
        queryset = TermCourse.objects.all()
        semester_id = self.request.query_params.get('semester_id')
        if semester_id:
            semester = Semester.objects.get(id=semester_id)
            queryset = queryset.filter(semester=semester)
        return queryset

class CourseDetailView(generics.RetrieveUpdateAPIView):
    queryset = TermCourse.objects.all()
    serializer_class = TermCourseSerializer
    lookup_field = 'slug'
    permission_classes = [
        IsCourseInstructor,
        IsCourseStudent,
        IsCourseStaff,
    ]
    

