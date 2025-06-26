# views.py (student)
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Q, Prefetch
from assessment.models import Assignment, Submission, Exam, Grade
from notifications.models import Announcement, Resource, AnnouncementWatch
from student_services.models import Enrollment, StudentProfile, Attendance
from academics.models import  Semester
from courses.models import TermCourse

from .serializers import ( 
    AssignmentSerializer, ExamSerializer, 
    ResourceSerializer, AnnouncementSerializer,
    AttendanceSerializer, StudentProfileSerializer,EnrollmentSerializer,
    GradeSerializer, SubmissionSerializer ,
    CourseEnrollmentSerializer, CourseSerializer
    
)

class StudentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 3  # Student

# StudentDashboard  SHOW[Student(Courses ,Assignment ,Exams ,Announcement ,Academic Profile.) ]
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

# Student Courses in Detail
class StudentCourseViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        student = self.request.user
        return TermCourse.objects.filter(
            enrollment__student=student,
            enrollment__is_active=True
        ).distinct().select_related('professor', 'course')

# Student Assignments in Detail with Submessions
class StudentAssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    serializer_class = AssignmentSerializer
    
    def get_queryset(self):
        student = self.request.user
        return Assignment.objects.filter(
            course__enrollment__student=student,
            course__enrollment__is_active=True
        ).select_related('course', 'course__course')
        # return Assignment.objects.filter(
        #     course__enrollment__student=student,
        #     course__enrollment__is_active=True
        # ).distinct().select_related('course', 'course__course')
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        assignment = self.get_object()
        submissions = Submission.objects.filter(
            assignment=assignment,
            student=request.user
        ).order_by('-submitted_at')
        serializer = SubmissionSerializer(
            submissions, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

# Student Submissons in Detail and Update/Delete
class StudentSubmissionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()
    
    def get_queryset(self):
        return Submission.objects.filter(
            student=self.request.user
        ).select_related('assignment', 'assignment__course')
    
    def create(self, request, *args, **kwargs):
        assignment_id = request.data.get('assignment')
        student = request.user
        
        # Validate assignment exists and student is enrolled
        assignment = Assignment.objects.filter(
            id=assignment_id,
            course__enrollment__student=student,
            course__enrollment__is_active=True
        ).first()
        
        if not assignment:
            return Response(
                {"error": "Invalid assignment or not enrolled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if submission is allowed
        if timezone.now() > assignment.due_date:
            return Response(
                {"error": "Submission deadline has passed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check attempt limit
        current_attempt = Submission.objects.filter(
            assignment=assignment,
            student=student
        ).count() + 1
        
        if current_attempt > assignment.max_attempts:
            return Response(
                {"error": "Maximum attempts exceeded"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create submission
        data = request.data.copy()
        data['student'] = student.id
        data['attempt_number'] = current_attempt
        data['is_late'] = timezone.now() > assignment.due_date
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#Student Enroll and Withdrow Course
class StudentEnrollmentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]

    @action(detail=False, methods=['post'])
    def enroll(self, request):
        student = request.user
        serializer = CourseEnrollmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        course_id = serializer.validated_data['course_id']
        course = TermCourse.objects.get(id=course_id)
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response(
                {"error": "Already enrolled in this course"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check registration period
        semester = course.semester
        today = timezone.now().date()
        if not (semester.registration_start <= today <= semester.registration_end):
            return Response(
                {"error": "Not within registration period"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check capacity
        if course.enrolled_students >= course.capacity:
            return Response(
                {"error": "Course is full"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student,
            course=course
        )
        
        # Update course enrollment count
        course.enrolled_students += 1
        course.save()
        
        return Response(
            {"success": f"Enrolled in {course.course.name}"},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        enrollment = Enrollment.objects.filter(
            id=pk,
            student=request.user,
            is_active=True
        ).first()
        
        if not enrollment:
            return Response(
                {"error": "Enrollment not found or already withdrawn"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check withdrawal deadline (example: 70% of semester passed)
        semester = enrollment.course.semester
        semester_duration = semester.end_date - semester.start_date
        days_passed = (timezone.now().date() - semester.start_date).days
        if days_passed / semester_duration.days > 0.7:
            return Response(
                {"error": "Withdrawal period has ended"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        enrollment.is_active = False
        enrollment.withdrawn = True
        enrollment.withdrawn_date = timezone.now()
        enrollment.save()
        
        # Update course enrollment count
        course = enrollment.course
        course.enrolled_students -= 1
        course.save()
        
        return Response(
            {"success": f"Withdrawn from {enrollment.course.course.name}"},
            status=status.HTTP_200_OK
        )

#Show All Student Grades
class StudentGradeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    serializer_class = GradeSerializer
    
    def get_queryset(self):
        return Grade.objects.filter(
            student=self.request.user,
            published=True
        ).select_related('exam', 'exam__course', 'exam__course__course')

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
                queryset=AnnouncementWatch.objects.filter(user=student),
                to_attr='student_views'
            )
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        student = request.user

        # Mark as viewed
        AnnouncementWatch.objects.get_or_create(
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
        return Resource.objects.filter(
            Q(is_public=True) |
            Q(course__enrollment__student=student, access_level='student') |
            Q(course__enrollment__student=student, access_level='ta')
        ).distinct().select_related('course', 'course__course')