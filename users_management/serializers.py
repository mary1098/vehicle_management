from django.db.models import fields
from rest_framework import serializers
from .models import Vehicle
from rest_framework.serializers import Serializer, IntegerField, CharField, ModelSerializer


class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["vehicle_id","vehicle_type", "vehicle_number", "vehicle_model", "vehicle_des"]


class VehicleCreateSerializer(Serializer):
    vehicle_type = CharField(max_length=50, required=True)
    vehicle_number = CharField(max_length=20, required=True)
    vehicle_model = CharField(max_length=100, required=True)
    vehicle_des = CharField(max_length=2000, required=True)


class VehicleUpdateSerializer(Serializer):
    vehicle_type = CharField(max_length=50, required=True)
    vehicle_number = CharField(max_length=20, required=True)
    vehicle_model = CharField(max_length=100, required=True)
    vehicle_des = CharField(max_length=200, required=True)


class VehicleGetSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["vehicle_number", "vehicle_model", "vehicle_des", "vehicle_type"]
