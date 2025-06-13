from rest_framework import generics, permissions
from .models import Course, CourseOffering
from .serializers import CourseSerializer, CourseOfferingSerializer
from academics.models import Semester
from django_filters.rest_framework import DjangoFilterBackend

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'is_core', 'is_active']
    search_fields = ['code', 'title']

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseOfferingListView(generics.ListCreateAPIView):
    serializer_class = CourseOfferingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'semester', 'instructor', 'is_active']

    def get_queryset(self):
        queryset = CourseOffering.objects.all()
        semester_id = self.request.query_params.get('semester_id')
        if semester_id:
            semester = Semester.objects.get(id=semester_id)
            queryset = queryset.filter(semester=semester)
        return queryset

class CourseOfferingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseOffering.objects.all()
    serializer_class = CourseOfferingSerializer
    permission_classes = [permissions.IsAuthenticated]