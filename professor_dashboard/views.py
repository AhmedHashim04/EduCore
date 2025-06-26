# views.py
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from assessment.models import Assignment, Submission, Exam
from notifications.models import Announcement, Resource
from student_services.models import Enrollment, Attendance
from courses.models import TermCourse
from users.models import User
from .serializers import (
TermCourseSerializer,EnrollmentSerializer,
AssignmentSerializer, ExamSerializer,
AnnouncementSerializer, ResourceSerializer,
SubmissionSerializer, CourseAnalyticsSerializer
)
from django.db.models import Count, Avg, Q, F
from django.utils import timezone

class ProfessorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 2  # Professor

class ProfessorCourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ProfessorPermission]
    serializer_class = TermCourseSerializer
    http_method_names = ['get']  # Read-only for courses

    def get_queryset(self):
        return TermCourse.objects.filter(
            instuctor=self.request.user
        ).select_related('semester', 'course').annotate(
            student_count=Count('enrollments', distinct=True),
            assignment_count=Count('assignments', distinct=True),
            exam_count=Count('exams', distinct=True)
        ).order_by('-semester__start_date')

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        course = self.get_object()
        enrollments = Enrollment.objects.filter(
            course=course
        ).select_related('student', 'student__profile')
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        course = self.get_object()
        
        # Calculate average grade
        avg_grade = Submission.objects.filter(
            assignment__course=course
        ).aggregate(avg_grade=Avg('grade'))['avg_grade'] or 0
        
        # Calculate assignment completion rate
        total_assignments = Assignment.objects.filter(course=course).count()
        completed_assignments = Submission.objects.filter(
            assignment__course=course,
            grade__isnull=False
        ).values('assignment').distinct().count()
        completion_rate = (completed_assignments / total_assignments * 100) if total_assignments else 0
        
        # Calculate attendance rate
        total_sessions = Attendance.objects.filter(course=course).count()
        present_sessions = Attendance.objects.filter(
            course=course, 
            status__in=['P', 'E']  # Present or Excused
        ).count()
        attendance_rate = (present_sessions / total_sessions * 100) if total_sessions else 0
        enrollments = Enrollment.objects.filter(
            course=course
        )

        data = {
            'course_id': course.id,
            'course_name': str(course),
            'student_count': enrollments.count(),
            'avg_grade': avg_grade,
            'assignment_completion': completion_rate,
            'attendance_rate': attendance_rate
        }
        
        serializer = CourseAnalyticsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class AssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ProfessorPermission]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()

    def get_queryset(self):
        return Assignment.objects.filter(
            course__instructor=self.request.user
        ).select_related('course', 'course__semester')

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.instructor != self.request.user:
            return Response(
                {"error": "You are not the professor for this course"},
                status=status.HTTP_403_FORBIDDEN
            )
        assignment = serializer.save()

        # Create empty submissions for all enrolled students
        students = User.objects.filter(
            enrollment__course=course,
            enrollment__is_active=True
        )
        submissions = [
            Submission(assignment=assignment, student=student)
            for student in students
        ]
        Submission.objects.bulk_create(submissions)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ExamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ProfessorPermission]
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()

    def get_queryset(self):
        return Exam.objects.filter(
            course__instructor=self.request.user
        ).select_related('course', 'course__semester')

class AnnouncementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ProfessorPermission]
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        # Get announcements created by professor or targeted to professors
        return Announcement.objects.filter(
            Q(created_by=self.request.user) |
            Q(target_audience='professors') |
            Q(target_audience='all')
        ).distinct().select_related('created_by', 'related_course')

class ResourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ProfessorPermission]
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def get_queryset(self):
        return Resource.objects.filter(
            uploaded_by=self.request.user
        ).select_related('course', 'uploaded_by')

class GradeSubmissionView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ProfessorPermission]
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()
    
    def perform_update(self, serializer):
        submission = self.get_object()
        if submission.assignment.course.instructor != self.request.user:
            return Response(
                {"error": "You are not authorized to grade this submission"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(
            grader=self.request.user,
            graded_at=timezone.now()
        )