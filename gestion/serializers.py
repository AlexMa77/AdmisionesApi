from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Facultad, Carrera, Docente, Estudiante, Materia, Matricula, Nota

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        fields = ["id", "nombre", "codigo", "descripcion", "activo", "creado_en"]


class CarreraSerializer(serializers.ModelSerializer):
    facultad_nombre = serializers.CharField(source="facultad.nombre", read_only=True)

    class Meta:
        model = Carrera
        fields = ["id", "facultad", "facultad_nombre", "nombre", "codigo",
                  "duracion_semestres", "activo", "creado_en"]


class DocenteSerializer(serializers.ModelSerializer):
    user_info = UserBasicSerializer(source="user", read_only=True)

    class Meta:
        model = Docente
        fields = ["id", "user", "user_info", "cedula", "telefono",
                  "especialidad", "activo", "creado_en"]


class EstudianteSerializer(serializers.ModelSerializer):
    user_info = UserBasicSerializer(source="user", read_only=True)
    carrera_nombre = serializers.CharField(source="carrera.nombre", read_only=True)

    class Meta:
        model = Estudiante
        fields = ["id", "user", "user_info", "carrera", "carrera_nombre",
                  "cedula", "telefono", "semestre_actual", "activo", "creado_en"]


class MateriaSerializer(serializers.ModelSerializer):
    carrera_nombre = serializers.CharField(source="carrera.nombre", read_only=True)
    docente_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Materia
        fields = ["id", "carrera", "carrera_nombre", "docente", "docente_nombre",
                  "nombre", "codigo", "creditos", "semestre", "activo", "creado_en"]

    def get_docente_nombre(self, obj):
        return obj.docente.user.get_full_name() or obj.docente.user.username


class MatriculaSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.SerializerMethodField()
    materia_nombre = serializers.CharField(source="materia.nombre", read_only=True)

    class Meta:
        model = Matricula
        fields = ["id", "estudiante", "estudiante_nombre", "materia", "materia_nombre",
                  "periodo", "estado", "fecha_matricula", "creado_en"]

    def get_estudiante_nombre(self, obj):
        return obj.estudiante.user.get_full_name() or obj.estudiante.user.username


class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ["id", "matricula", "parcial1", "parcial2", "examen_final",
                  "nota_final", "aprobado", "actualizado_en"]
        read_only_fields = ["nota_final", "aprobado", "actualizado_en"]
