from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Facultad(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True, default="")
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Carrera(models.Model):
    facultad = models.ForeignKey(Facultad, on_delete=models.PROTECT, related_name="carreras")
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=20, unique=True)
    duracion_semestres = models.IntegerField(
        default=8,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="docente")
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True, default="")
    especialidad = models.CharField(max_length=150, blank=True, default="")
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.cedula})"


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="estudiante")
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT, related_name="estudiantes")
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True, default="")
    semestre_actual = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.cedula})"


class Materia(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT, related_name="materias")
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name="materias")
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=20, unique=True)
    creditos = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    semestre = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["semestre", "nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Matricula(models.Model):
    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        RETIRADA = "retirada", "Retirada"
        FINALIZADA = "finalizada", "Finalizada"

    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT, related_name="matriculas")
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, related_name="matriculas")
    periodo = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVA)
    fecha_matricula = models.DateField(auto_now_add=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["estudiante", "materia", "periodo"]
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.estudiante} - {self.materia} ({self.periodo})"


class Nota(models.Model):
    matricula = models.OneToOneField(Matricula, on_delete=models.CASCADE, related_name="nota")
    parcial1 = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    parcial2 = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    examen_final = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    nota_final = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    aprobado = models.BooleanField(null=True, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        notas = [n for n in [self.parcial1, self.parcial2, self.examen_final] if n is not None]
        if len(notas) == 3:
            self.nota_final = round(sum(float(n) for n in notas) / 3, 2)
            self.aprobado = self.nota_final >= 7.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Nota de {self.matricula}"
