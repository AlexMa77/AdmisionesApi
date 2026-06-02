from django.contrib import admin
from .models import Facultad, Carrera, Docente, Estudiante, Materia, Matricula, Nota


@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nombre", "activo", "creado_en"]
    search_fields = ["nombre", "codigo"]
    list_filter = ["activo"]


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nombre", "facultad", "duracion_semestres", "activo"]
    search_fields = ["nombre", "codigo"]
    list_filter = ["activo", "facultad"]


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ["cedula", "user", "especialidad", "activo", "creado_en"]
    search_fields = ["cedula", "user__first_name", "user__last_name", "user__username"]
    list_filter = ["activo"]


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ["cedula", "user", "carrera", "semestre_actual", "activo"]
    search_fields = ["cedula", "user__first_name", "user__last_name", "user__username"]
    list_filter = ["activo", "carrera"]


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nombre", "carrera", "docente", "semestre", "creditos", "activo"]
    search_fields = ["nombre", "codigo"]
    list_filter = ["activo", "carrera", "semestre"]


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ["estudiante", "materia", "periodo", "estado", "fecha_matricula"]
    list_filter = ["estado", "periodo"]
    search_fields = ["periodo"]


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ["matricula", "parcial1", "parcial2", "examen_final", "nota_final", "aprobado"]
    list_filter = ["aprobado"]
