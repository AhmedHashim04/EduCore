from rest_framework import viewsets, generics, status, permissions

from .models import TermCourse
from .serializers import CourseSerializer, CourseEnrollmentSerializer
from users.permissions import StudentPermission
from student_services.models import Enrollment

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action
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
