from django.db import models
from .validators import FileValidator
from accounts.models import Account

# Create your models here.
class Desk(models.Model):
    desk_id =  models.CharField(max_length=16)
    name =  models.CharField(max_length=16)
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)



validate_file = FileValidator(max_size=1024 * 5000,
                             content_types=('image/jpeg','image/png','image/gif','image/tiff','application/x-empty',))


def image_path_handler(instance, filename):
    fn, ext = os.path.splitext(filename)
    #Create a random filename using hash function
    name = secrets.token_hex(20)
    print("uploading",instance.__dict__)
    return "titleimage_{id}/{name}.png".format(id=instance.id,name=name)



#For booking
class Slot(models.Model):
    date = models.DateTimeField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date'], name='unique_slot')
        ]


class Booking(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot,on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk,on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot','desk','user'], name='unique_booking')
        ]


class Organisation(models.Model):
     owner = models.ForeignKey(Account,on_delete=models.CASCADE)
     name = models.CharField(max_length=200)
     org_id = models.CharField(max_length=16)

#One organisation to many employees
class OrgEmployee(models.Model):
    employee = models.ForeignKey(Account,on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee','organisation'], name='unique_org_emp')
        ]


class Building(models.Model):
    organisation = models.ForeignKey(Organisation,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Floor(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField()
    building = models.ForeignKey(Building,on_delete=models.CASCADE)


#Represents the floor plan
class Plan(models.Model):
    floor = models.ForeignKey(Floor,on_delete=models.CASCADE)
    creator = models.ForeignKey(Account,on_delete=models.CASCADE)
    picture = models.FileField(upload_to=image_path_handler)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

#Relationship between desk and floor plan
class DeskPlan(models.Model):
    desk = models.ForeignKey(Desk,on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['desk','plan'], name='unique_desk_plan')
        ]
