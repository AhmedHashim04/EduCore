from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import ProfileSerializer


User = get_user_model()


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
