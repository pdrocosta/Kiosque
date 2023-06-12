from rest_framework import serializers
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer
from .models import SexOptions


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()
    weight = serializers.IntegerField()
    sex = serializers.ChoiceField(choices=SexOptions, default=SexOptions.DEFAULT)
