from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Facultad, Carrera, Docente, Estudiante, Materia, Matricula, Nota
from .serializers import (
    FacultadSerializer, CarreraSerializer, DocenteSerializer,
    EstudianteSerializer, MateriaSerializer, MatriculaSerializer, NotaSerializer,
)
from .permissions import IsAdminOrReadOnly


class FacultadViewSet(viewsets.ModelViewSet):
    queryset = Facultad.objects.all()
    serializer_class = FacultadSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["activo"]
    search_fields = ["nombre", "codigo"]
    ordering_fields = ["id", "nombre", "codigo"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()


class CarreraViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.select_related("facultad").all()
    serializer_class = CarreraSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["activo", "facultad"]
    search_fields = ["nombre", "codigo"]
    ordering_fields = ["id", "nombre", "codigo"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()


class DocenteViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.select_related("user").all()
    serializer_class = DocenteSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["activo"]
    search_fields = ["cedula", "especialidad", "user__first_name", "user__last_name"]
    ordering_fields = ["id", "cedula"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return super().get_permissions()


class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.select_related("user", "carrera").all()
    serializer_class = EstudianteSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["activo", "carrera", "semestre_actual"]
    search_fields = ["cedula", "user__first_name", "user__last_name"]
    ordering_fields = ["id", "cedula", "semestre_actual"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return super().get_permissions()


class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.select_related("carrera", "docente__user").all()
    serializer_class = MateriaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["activo", "carrera", "semestre", "docente"]
    search_fields = ["nombre", "codigo"]
    ordering_fields = ["id", "nombre", "semestre", "codigo"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return super().get_permissions()


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.select_related("estudiante__user", "materia").all()
    serializer_class = MatriculaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["estado", "periodo", "estudiante", "materia"]
    search_fields = ["periodo"]
    ordering_fields = ["id", "periodo", "fecha_matricula"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return super().get_permissions()


class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.select_related(
        "matricula__estudiante__user", "matricula__materia"
    ).all()
    serializer_class = NotaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["aprobado", "matricula"]
    ordering_fields = ["id", "nota_final", "actualizado_en"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return super().get_permissions()


from django.contrib.auth import get_user_model
from .serializers import UserBasicSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserBasicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["username", "first_name", "last_name", "email"]

