from django.db import models

# Create your models here.

class Student(models.Model):
    name        = models.CharField(max_length=25)
    roll_number = models.IntegerField(unique=True, primary_key=True)

    def __str__(self) -> str:
        return self.name

class Performance(models.Model):
    student_id    = models.OneToOneField(to=Student, on_delete=models.CASCADE, unique=True, primary_key=True)
    maths_marks   = models.DecimalField(max_digits=4, decimal_places=1 , db_index=True)
    science_marks = models.DecimalField(max_digits=4, decimal_places=1 , db_index=True)
    english_marks = models.DecimalField(max_digits=4, decimal_places=1 , db_index=True)
    CS_marks      = models.DecimalField(max_digits=4, decimal_places=1 , db_index=True)
    total_marks   = models.DecimalField(max_digits=4, decimal_places=1 , db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.total_marks = self.maths_marks + self.science_marks + self.english_marks + self.CS_marks
        super(Performance, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.student_id
    