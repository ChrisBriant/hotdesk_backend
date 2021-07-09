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


class FloorSerializer(serializers.ModelSerializer):
    plan_id = serializers.ReadOnlyField(source='plan.id')

    class Meta:
        model = Floor
        fields = ('id','level','name','plan_id')


class BuildingSerializer(serializers.ModelSerializer):
    floor = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = ('id','name','floor')

    def get_floor(self,obj):
        floor_data = obj.floor_set.all()
        return FloorSerializer(floor_data,many=True).data
