from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from models import Pet
from serializers import *
from traits.models import Trait
from groups.models import Group



class PetsView(APIView):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(instance=result_page, many=True)
        return self.get_paginated_reponse(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetResSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        traits_data = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")
        pet = Pet.objects.create(**serializer.validated_data)

        for trait in traits_data:
            trait_data = Trait.object.filter(
                trait_name__iexact=trait["trait_name"]
            ).first()

            if not trait_data:
                trait_data = Trait.objects.create(**trait)

            pet.traits.add(trait_data)

        for group in group_data:
            group_data = Group.object.filter(
                scientific_name__iexact=trait["scientific_name"]
            ).first()

            if not group_data:
                group_data = Group.objects.create(**group)

            pet.group.add(group_data)

        serializer = PetSerializer(instace=pet)
        return Response(serializer.data, 201)


class PetsIdView(APIView):
    def get(self, request: Request) -> Response:
        def delete(self, request: Request) -> Response:
    def patch(self, request: Request) -> Response:
    