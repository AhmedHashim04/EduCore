# views.py (student)
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Q, Prefetch
from assessment.models import Assignment, Submission, Exam, Grade
from notifications.models import Announcement, AnnouncementAttachment, AnnouncementView
from student_services.models import Enrollment, StudentProfile, Attendance
from academics.models import  Semester
from courses.models import TermCourse

from .serializers import ( 
    AssignmentSerializer, ExamSerializer, 
    ResourceSerializer, AnnouncementSerializer,
    AttendanceSerializer, StudentProfileSerializer,EnrollmentSerializer,

    
)
from users.permissions import StudentPermission
class StudentDashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    
    def get(self, request):
        student = request.user
        current_semester = Semester.objects.filter(is_current=True).first()
        
        # Get active enrollments
        enrollments = Enrollment.objects.filter(
            student=student, 
            is_active=True,
            course__semester=current_semester
        ).select_related('course', 'course__professor')
        
        # Get upcoming deadlines
        upcoming_assignments = Assignment.objects.filter(
            course__enrollment__student=student,
            due_date__gt=timezone.now()
        ).order_by('due_date')[:5]
        
        upcoming_exams = Exam.objects.filter(
            course__enrollment__student=student,
            date__gt=timezone.now()
        ).order_by('date')[:5]
        
        # Get unread announcements
        unread_announcements = Announcement.objects.filter(
            Q(target_audience='all') | 
            Q(target_audience='students') |
            Q(related_course__enrollment__student=student)
        ).exclude(
            views__student=student
        ).distinct()[:5]
        
        # Get academic standing
        profile = StudentProfile.objects.get(student=student)
        
        data = {
            'enrollments': EnrollmentSerializer(enrollments, many=True).data,
            'upcoming_assignments': AssignmentSerializer(
                upcoming_assignments, 
                many=True,
                context={'request': request}
            ).data,
            'upcoming_exams': ExamSerializer(
                upcoming_exams, 
                many=True,
                context={'request': request}
            ).data,
            'unread_announcements': AnnouncementSerializer(
                unread_announcements, 
                many=True,
                context={'request': request}
            ).data,
            'academic_profile': StudentProfileSerializer(profile).data
        }
        
        return Response(data)

#Show Student Attendance
class StudentAttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    serializer_class = AttendanceSerializer
    
    def get_queryset(self):
        return Attendance.objects.filter(
            student=self.request.user
        ).select_related('course', 'course__course')

#Student Announcements and Announcement Watched
class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        student = self.request.user
        return Announcement.objects.filter(
            Q(target_audience='all') | 
            Q(target_audience='students') |
            Q(related_course__enrollment__student=student)
        ).distinct().prefetch_related(
            Prefetch(
                'views',
                queryset=AnnouncementView.objects.filter(user=student),
                to_attr='student_views'
            )
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = request.user

        # Mark as viewed
        AnnouncementView.objects.get_or_create(
            announcement=instance,
            user=student,
            defaults={'viewed_at': timezone.now()}
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class StudentResourceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    serializer_class = ResourceSerializer
    
    def get_queryset(self):
        student = self.request.user
        return AnnouncementAttachment.objects.filter(
            Q(is_public=True) |
            Q(course__enrollment__student=student, access_level='student') |
            Q(course__enrollment__student=student, access_level='ta')
        ).distinct().select_related('course', 'course__course')