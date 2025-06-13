from rest_framework import generics, permissions
from .models import ProfessorProfile
from .serializers import ProfessorProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ProfessorProfileListView(generics.ListAPIView):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department']

class ProfessorProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]