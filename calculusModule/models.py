from django.db import models
from django.contrib.auth.models import User as DjangoUser
import locale

class Week(models.Model):
    dateStart = models.DateField(null=False, blank=False, verbose_name="Date de début")
    dateEnd = models.DateField(null=False, blank=False, verbose_name="Date de fin")
    displayNumber = models.IntegerField(null=False, blank=True, unique=True, verbose_name="Numéro de la semaine")

    def __str__(self):
        return f"Semaine {self.displayNumber} {self.displayDates()}"
    
    def fullInlineDisplay(self):
        return f"semaine {self.displayNumber} {self.displayDates()}"
    
    def displayDates(self):
        locale.setlocale(locale.LC_TIME, "fr_FR.utf8")
        if self.dateStart.month == self.dateEnd.month:
            return f'du {self.dateStart.day} au {self.dateEnd.day} {self.dateStart.strftime("%B")}'
        else:
            return f'du {self.dateStart.day} {self.dateStart.strftime("%B")} au {self.dateEnd.day} {self.dateEnd.strftime("%B")}'
    
class SchoolClassLevel(models.TextChoices):
    CM2 = "CM2", "CM2"
    SIXIEME = "SIXIEME", "Sixieme"

class SchoolClass(models.Model):
    teacher = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Enseignant")
    level = models.CharField(max_length=16, choices = SchoolClassLevel.choices, default=SchoolClassLevel.CM2, null=False, blank=False, verbose_name="Niveau scolaire")
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name="Nom de la classe")

    def __str__(self):
        return f"{self.name} ({self.level})"

class Score(models.Model):
    schoolClass = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Classe")
    week = models.ForeignKey(Week, on_delete=models.CASCADE, null=False, blank=False, verbose_name="Semaine")
    numericScore = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2, verbose_name="Score")
    nullScoresPercentage = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=1, verbose_name="Pourcentage de scores nuls")
    mathadorsPercentage = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=1, verbose_name="Pourcentage de Mathadors")

    class Meta:
        unique_together = (("schoolClass","week"),)

    def __str__(self):
        return f"{self.schoolClass} - {self.week}"