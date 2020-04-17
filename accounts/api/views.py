from rest_framework import viewsets
# from rest_framework.response import Response
from accounts.api.serializers import UserSerializer, DoctorSerializer, PatientSerializer
from accounts.models import Doctor, Patient
from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(User,
                                 email=self.request.user.email) if self.action == 'current' else super().get_object()

    @action(methods=['get'], detail=False)
    def current(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
