from rest_framework import serializers


class AsistenciaSerializer(serializers.Serializer):
    matricula_id = serializers.IntegerField()
    materia_id = serializers.IntegerField()
    estudiante_id = serializers.IntegerField()
    fecha = serializers.DateField()
    presente = serializers.BooleanField(default=True)
    observacion = serializers.CharField(required=False, allow_blank=True, default="")


class ActividadSerializer(serializers.Serializer):
    TIPO_CHOICES = [
        ("tarea", "Tarea"),
        ("examen", "Examen"),
        ("proyecto", "Proyecto"),
        ("anuncio", "Anuncio"),
    ]

    materia_id = serializers.IntegerField()
    titulo = serializers.CharField(max_length=200)
    descripcion = serializers.CharField(required=False, allow_blank=True, default="")
    tipo = serializers.ChoiceField(choices=TIPO_CHOICES, default="tarea")
    fecha_limite = serializers.DateField(required=False, allow_null=True)
    creado_por = serializers.IntegerField(required=False, allow_null=True)
    activo = serializers.BooleanField(default=True)
