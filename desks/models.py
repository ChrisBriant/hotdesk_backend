from django.db import models
from django.dispatch import receiver
from django.conf import settings
from .validators import FileValidator
from accounts.models import Account
import os, secrets




validate_file = FileValidator(max_size=1024 * 5000,
                             content_types=('image/jpeg','image/png','image/gif','image/tiff','application/x-empty',))


def image_path_handler(instance, filename):
    fn, ext = os.path.splitext(filename)
    #Create a random filename using hash function
    name = secrets.token_hex(20)
    print("uploading",instance.__dict__)
    return "plan_{id}/{name}.png".format(id=instance.floor_id,name=name)





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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['floor'], name='unique_floor')
        ]


@receiver(models.signals.post_delete, sender=Plan)
def delete_image(sender, instance, *args, **kwargs):
    os.remove(instance.picture.path)

@receiver(models.signals.post_save, sender=Plan)
def clear_images(sender, instance, *args, **kwargs):
    dir = os.path.dirname(instance.picture.path)
    files = os.listdir(dir)
    file = os.path.basename(instance.picture.path)
    [os.remove(dir+'/'+f) for f in files if f != file]


#Relationship between desk and floor plan
# class DeskPlan(models.Model):
#     desk = models.ForeignKey(Desk,on_delete=models.CASCADE)
#     plan = models.ForeignKey(Plan,on_delete=models.CASCADE)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['desk','plan'], name='unique_desk_plan')
#         ]

class Desk(models.Model):
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE)
    desk_id =  models.CharField(max_length=16)
    name =  models.CharField(max_length=16)
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
