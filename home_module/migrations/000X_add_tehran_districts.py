from django.db import migrations

def add_tehran_districts(apps,schema_editor):
    City = apps.get_model("iranian_cities","City")
    TehranDistrict = apps.get_model("home_module","TehranDistrict")
    
    
    tehran, created = City.objects.get_or_create(name = "تهران")
    
    district_names=[
                "منطقه 1",
                "منطقه 2",
                "منطقه 3",
                "منطقه 4",
                "منطقه 5",
                "منطقه 6",
                "منطقه 7",
                "منطقه 8",
                "منطقه 9",
                "منطقه 10",
                "منطقه 11",
                "منطقه 12",
                "منطقه 13",
                "منطقه 14",
                "منطقه 15",
                "منطقه 16",
                "منطقه 17",
                "منطقه 18",
                "منطقه 19",
                "منطقه 20",
                "منطقه 21",
                "منطقه 22",
    ]
    
    for district_name in district_names:
        TehranDistrict.objects.get_or_create(name = district_name,city = tehran)

class Migration(migrations.Migration):
    dependencies = [
        ("home_module","0001_initial")
    ]
    operations =[
        migrations.RunPython(add_tehran_districts),
    ]
    