from django.db import models


# Create your models here.
class Vehicle(models.Model):
    type_choice = (
        ('None', 'None'),
        ('Two Wheeler', 'Two Wheeler'),
        ('Three Wheeler', 'Three Wheeler'),
        ('Four Wheeler', 'Four Wheeler'),
    )
    vehicle_id = models.AutoField(primary_key=True, editable=False, blank=False, null=False)
    is_active = models.IntegerField(default=1, null=False, blank=False)
    is_delete = models.IntegerField(default=0, null=False, blank=False)
    vehicle_number = models.CharField(max_length=20, blank=False, null=False)
    vehicle_model = models.TextField(max_length=100, blank=False, null=False)
    vehicle_des = models.TextField(max_length=2000, blank=False, null=False)
    vehicle_type = models.CharField(max_length=50, blank=True, null=False, choices=type_choice, default='None')

    def __str__(self):
        return str(self.vehicle_number, self.vehicle_model, self.vehicle_des, self.vehicle_type)
