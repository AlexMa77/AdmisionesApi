from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    FacultadViewSet, CarreraViewSet, DocenteViewSet,
    EstudianteViewSet, MateriaViewSet, MatriculaViewSet, NotaViewSet,
    UserViewSet,
)
from .asistencia_views import asistencias_list_create, asistencias_detail
from .actividades_views import actividades_list_create, actividades_detail
from .health import health_check

router = DefaultRouter()
router.register(r"facultades", FacultadViewSet, basename="facultad")
router.register(r"carreras", CarreraViewSet, basename="carrera")
router.register(r"docentes", DocenteViewSet, basename="docente")
router.register(r"estudiantes", EstudianteViewSet, basename="estudiante")
router.register(r"materias", MateriaViewSet, basename="materia")
router.register(r"matriculas", MatriculaViewSet, basename="matricula")
router.register(r"notas", NotaViewSet, basename="nota")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("health/", health_check),
    path("asistencias/", asistencias_list_create),
    path("asistencias/<str:id>/", asistencias_detail),
    path("actividades/", actividades_list_create),
    path("actividades/<str:id>/", actividades_detail),
]

urlpatterns += router.urls
