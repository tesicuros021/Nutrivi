from django.db import models
import random

class Patients(models.Model):
    ime = models.CharField(max_length=255)
    prezime = models.CharField(max_length=255)
    datum_rodjenja = models.DateField()
    pol = models.CharField(max_length=10)
    kontakt_telefon = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    adresa = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.ime} {self.prezime}"
    
    patient_id = models.CharField(max_length=6, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Generate a random 6-digit number as a string
            self.patient_id = str(random.randint(100000, 999999))

            # Ensure the generated ID is unique
            while Patients.objects.filter(patient_id=self.patient_id).exists():
                self.patient_id = str(random.randint(100000, 999999))

        super(Patients, self).save(*args, **kwargs)


class Meetings(models.Model):
    patient_meeting_id = models.IntegerField(editable=False)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    datum_sastanka = models.DateField(null=True, blank=True)  # Allow null and blank
    dijagnoza_za_ishranu = models.TextField(blank=True, null=True)
    preporuka_za_ishranu = models.TextField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)
    telesna_masa = models.FloatField(blank=True, null=True)
    visina = models.FloatField(blank=True, null=True)
    procenat_spoljasnje_masti = models.FloatField(blank=True, null=True)
    procenat_unutrasnje_masti = models.FloatField(blank=True, null=True)
    procenat_misica = models.FloatField(blank=True, null=True)
    procenat_vode = models.FloatField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new instance
            max_id = Meetings.objects.filter(patient=self.patient).aggregate(models.Max('patient_meeting_id'))['patient_meeting_id__max']
            self.patient_meeting_id = (max_id or 0) + 1
        super(Meetings, self).save(*args, **kwargs)

    def generate_meeting_id(self):
        last_meeting = Meetings.objects.order_by('-meeting_id').first()
        if last_meeting:
            return last_meeting.meeting_id + 1
        else:
            return 1