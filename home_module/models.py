from django.db import models
from iranian_cities.models import City
# Create your models here.

class TehranDistrict(models.Model):
    
    TEHRAN_DISTRICT = (
        ("1","منطقه 1"),
        ("2","منطقه 2"),
        ("3","منطقه 3"),
        ("4","منطقه 4"),
        ("5","منطقه 5"),
        ("6","منطقه 6"),
        ("7","منطقه 7"),
        ("8","منطقه 8"),
        ("9","منطقه 9"),
        ("10","منطقه 10"),
        ("11","منطقه 11"),
        ("12","منطقه 12"),
        ("13","منطقه 13"),
        ("14","منطقه 14"),
        ("15","منطقه 15"),
        ("16","منطقه 16"),
        ("17","منطقه 17"),
        ("18","منطقه 18"),
        ("19","منطقه 19"),
        ("20","منطقه 20"),
        ("21","منطقه 21"),
        ("22","منطقه 22"),
    )
    
    city = models.ForeignKey(City,on_delete=models.CASCADE,verbose_name="نام شهر",related_name="districts")
    name = models.CharField(max_length=220,verbose_name="نام منطقه",unique=True)
    
    class Meta:
        verbose_name = 'منطقه'
        verbose_name_plural = 'مناطق'
        
    def __str__(self):
        return self.name