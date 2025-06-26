from rest_framework import generics, permissions
from .models import Assignment, Submission, Exam, Grade
from .serializers import (
    AssignmentSerializer, SubmissionSerializer,
    ExamSerializer, GradeSerializer
)
from courses.models import TermCourse
from django_filters.rest_framework import DjangoFilterBackend

class AssignmentListView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course_offering']

    def get_queryset(self):
        queryset = Assignment.objects.all()
        course_offering_id = self.request.query_params.get('course_offering_id')
        if course_offering_id:
            course_offering = TermCourse.objects.get(id=course_offering_id)
            queryset = queryset.filter(course_offering=course_offering)
        return queryset

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmissionListView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assignment', 'student']

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class SubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExamListView(generics.ListCreateAPIView):
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course_offering', 'exam_type']

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

class GradeListView(generics.ListCreateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exam', 'student']

class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]