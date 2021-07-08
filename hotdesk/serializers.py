from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.db.models import Count, Avg
from accounts.models import Account
from desks.models import *
from django.conf import settings

class GeneralResponse(object):
    def __init__(self, success, message):
        self.success = success
        self.message = message

class ResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=100)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','email','name')

#Restrict publicly viewable user attributes
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','name')

class OrganisationSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    memberships = serializers.SerializerMethodField()

    class Meta:
        model = Organisation
        fields = ('id','org_id','name','is_admin','memberships')

    def get_is_admin(self,obj):
        print(self.context)
        if self.context['user'] == obj.owner:
            return True
        else:
            return False

    def get_memberships(self,obj):
        print(self.context)
        if self.context['user'] == obj.owner:
            return EmployeeMemberSerializer(obj.orgemployee_set,many=True,context=self.context).data
        else:
            return []


class OrgEmployeeSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer()
    is_owner = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = OrgEmployee
        fields = ('id','organisation','is_owner','status')

    def get_is_owner(self,obj):
        print(obj.organisation.owner.id,self.context['user'].id)
        if obj.organisation.owner == self.context['user']:
            return True
        else:
            return False

    def get_status(self,obj):
        print(obj.organisation.owner.id,self.context['user'].id)
        if not obj.organisation.owner == self.context['user']:
            if obj.approved:
                return 'Approved'
            else:
                return 'Awaiting Approval'
        else:
            return 'Admin'




class EmployeeMemberSerializer(serializers.ModelSerializer):
    employee_data = serializers.SerializerMethodField()

    class Meta:
        model = OrgEmployee
        fields = ('id','approved','employee_data')

    def get_employee_data(self,obj):
        return EmployeeSerializer(obj.employee).data

# class CatSerializer(serializers.ModelSerializer):
#     cat_picture = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Cat
#         fields = ('id','name','age','food','toy','color','breed','cat_picture')
#
#     def get_cat_picture(self,obj):
#         try:
#             return "{0}{1}".format(settings.BASE_URL[:-1], obj.picture.url)
#         except Exception as e:
#             return None
#
# class TableSerializer(serializers.ModelSerializer):
#     booking_id = serializers.ReadOnlyField(source='id')
#
#     class Meta:
#         model = Table
#         fields = ('booking_id','table_number')
#
#     time = serializers.SerializerMethodField()
#     date_str = serializers.SerializerMethodField()
#     table_set =  serializers.SerializerMethodField()
#
#     class Meta:
#         model = Slot
#         fields = ('id','table_set','time','date','date_str','date_booked','date_modified')
#
#     def get_time(self,obj):
#         return obj.date.strftime("%H:%M")
#
#     #Helper for front end - friendly format so the date can be naive in JS code
#     def get_date_str(self,obj):
#         return obj.date.strftime("%Y-%m-%d %H:%M")
#
#     def get_table_set(self,obj):
#         return TableSerializer(obj.table_set.order_by('table_number'),many=True).data
#
#
# class MonthSlotSerializer(serializers.Serializer):
#     # intialize fields
#     dictionary = serializers.DictField(
#     child = serializers.CharField())
