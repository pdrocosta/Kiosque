from rest_framework import serializers
from models import SexOptions
from traits.serializers import TraitSerializer, TraitResSerializer
from groups.serializers import GroupSerializer, GroupResSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
    weight = serializers.IntegerField()
    sex = serializers.ChoiceField(choices=SexOptions, default=SexOptions.DEFAULT)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)


class PetResSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
    weight = serializers.IntegerField()
    sex = serializers.ChoiceField(choices=SexOptions, default=SexOptions.DEFAULT)
    group = GroupResSerializer()
    traits = TraitResSerializer(many=True)
