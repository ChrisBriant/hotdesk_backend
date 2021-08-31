from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.db.models import Count, Avg
from accounts.models import Account
from desks.models import *
from booking.models import *
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

#Just return id and name for privacy
class EmployeeSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','name')

class EmployeeMemberSerializer(serializers.ModelSerializer):
    employee_data = serializers.SerializerMethodField()

    class Meta:
        model = OrgEmployee
        fields = ('id','approved','employee_data')

    def get_employee_data(self,obj):
        return EmployeeSerializer(obj.employee).data

#Restrict publicly viewable user attributes
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','name')

class DeskSerializer(serializers.ModelSerializer):
    desk_floor = serializers.SerializerMethodField()
    desk_building = serializers.SerializerMethodField()

    class Meta:
        model = Desk
        fields = ('id','desk_id','name','x','y','w','h','desk_floor',
            'desk_building')

    def get_desk_floor(self,obj):
        return obj.plan.floor.name

    def get_desk_building(self,obj):
        return obj.plan.floor.building.name

class PlanSerializer(serializers.ModelSerializer):
    desks = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ('id','picture','desks')

    def get_desks(self,obj):
        return DeskSerializer(obj.desk_set.all(),many=True).data


class FloorSerializer(serializers.ModelSerializer):
    plan_id = serializers.ReadOnlyField(source='plan.id')
    plan = serializers.SerializerMethodField()

    class Meta:
        model = Floor
        fields = ('id','level','name','plan_id','plan')

    def get_plan(self,obj):
        plan_data = obj.plan_set.all()
        if len(plan_data) > 0:
            return PlanSerializer(obj.plan_set.all()[0]).data
        else:
            return None


class BuildingSerializer(serializers.ModelSerializer):
    floor = serializers.SerializerMethodField()

    class Meta:
        model = Building
        fields = ('id','name','floor')

    def get_floor(self,obj):
        floor_data = obj.floor_set.all()
        return FloorSerializer(floor_data,many=True).data


class OrganisationSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()
    memberships = serializers.SerializerMethodField()
    buildings = serializers.SerializerMethodField()
    owner = EmployeeSerializerSimple()

    class Meta:
        model = Organisation
        fields = ('id','org_id','name','is_admin','memberships','buildings','owner')

    def get_is_admin(self,obj):
        if self.context['user'] == obj.owner:
            return True
        else:
            return False

    def get_memberships(self,obj):
        if self.context['user'] == obj.owner:
            return EmployeeMemberSerializer(obj.orgemployee_set,many=True,context=self.context).data
        else:
            return []

    def get_buildings(self,obj):
        buildings = obj.building_set.all()
        return BuildingSerializer(buildings,many=True).data


class OrgEmployeeSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer()
    is_owner = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = OrgEmployee
        fields = ('id','organisation','is_owner','status')

    def get_is_owner(self,obj):
        if obj.organisation.owner == self.context['user']:
            return True
        else:
            return False

    def get_status(self,obj):
        if not obj.organisation.owner == self.context['user']:
            if obj.approved:
                return 'Approved'
            else:
                return 'Awaiting Approval'
        else:
            return 'Admin'


class BookingSerializer(serializers.ModelSerializer):
    user = EmployeeSerializer()
    desk = DeskSerializer()
    date_str = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ('id','user',
        'desk','date','date_str')

    def get_date_str(self,obj):
        return obj.date.strftime("%d/%m/%Y")
