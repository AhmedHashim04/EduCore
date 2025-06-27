from rest_framework import generics, permissions, viewsets,status
from .models import Assignment, Submission, Exam, Grade
from .serializers import StudentAssignmentSerializer, StudentSubmissionSerializer, StudentExamSerializer, StudentGradeSerializer
from .serializers import ProfessorAssignmentSerializer, ProfessorSubmissionSerializer, ProfessorExamSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from users.permissions import StudentPermission, ProfessorPermission
from users.models import User

class StudentAssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    serializer_class = StudentAssignmentSerializer
    
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
    serializer_class = StudentSubmissionSerializer
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

#Show All Student Grades
class StudentGradeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StudentPermission]
    serializer_class = StudentGradeSerializer
    
    def get_queryset(self):
        return Grade.objects.filter(
            student=self.request.user,
            published=True
        ).select_related('exam', 'exam__course', 'exam__course__course')

class AssignmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ProfessorPermission]
    serializer_class = StudentAssignmentSerializer
    queryset = Assignment.objects.all()

    def get_queryset(self):
        return Assignment.objects.filter(
            course__professor=self.request.user
        ).select_related('course', 'course__semester')

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.professor != self.request.user:
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
    permission_classes = [permissions.IsAuthenticated, ProfessorPermission]
    serializer_class = ProfessorExamSerializer
    queryset = Exam.objects.all()

    def get_queryset(self):
        return Exam.objects.filter(
            course__professor=self.request.user
        ).select_related('course', 'course__semester')

class GradeSubmissionView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ProfessorPermission]
    serializer_class = ProfessorSubmissionSerializer
    queryset = Submission.objects.all()
    
    def perform_update(self, serializer):
        submission = self.get_object()
        if submission.assignment.course.professor != self.request.user:
            return Response(
                {"error": "You are not authorized to grade this submission"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(
            grader=self.request.user,
            graded_at=timezone.now()
        )