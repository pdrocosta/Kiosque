from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Pet
from .serializers import PetSerializer
from traits.models import Trait
from groups.models import Group


class PetsView(APIView):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        query_trait = request.query_params.get("trait", None)
        if query_trait:
            pets = Pet.objects.filter(
                traits=query_trait
            )
        result_page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(instance=result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        traits_data = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")
        pet = Pet.objects.create(**serializer.validated_data)

        for trait in traits_data:
            trait_data = Trait.objects.get_or_create(
                trait_name__iexact=trait["trait_name"],
                defaults=trait
            )
            pet.traits.add(trait_data)

        for group in group_data:
            group_data = Group.objects.get_or_create(
                scientific_name__iexact=group["scientific_name"],
                defaults=group
            )
            pet.group.add(group_data)

        serializer = PetSerializer(instace=pet)
        return Response(serializer.data, status=201)


class PetsIdView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        try:
            pet = get_object_or_404(Pet, id=pet_id)
            serializer = PetSerializer(instance=pet)
            return Response(data=serializer, status=200)
        except ObjectDoesNotExist:
            return Response(data={"detail": "Not found."}, status=404)

    def delete(self, request: Request,  pet_id: int) -> Response:
        try:
            pet = get_object_or_404(Pet, id=pet_id)
            pet.delete()
            return Response(status=204)
        except ObjectDoesNotExist:
            return Response(data={"detail": "Not found."}, status=404)

    def patch(self, request: Request, pet_id: int) -> Response:
        try:
            pet = get_object_or_404(Pet, id=pet_id)
            serializer = PetSerializer(instance=pet, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
        except ObjectDoesNotExist:
            return Response(data={"detail": "Not found."}, status=404)

        traits_data = serializer.validated_data.pop("traits", None) 
        group_data = serializer.validated_data.pop("group", None)

        if traits_data:
            pet.traits.clear()
            for trait in traits_data:
                trait_data = Trait.objects.get_or_create(
                    trait_name__iexact=trait["trait_name"], defaults=trait)
            pet.traits.add(trait_data)

        if group_data:
            pet.group.remove()
            group = Group.objects.get_or_create(
                scientific_name__iexact=group["scientific_name"],
                defaults=group)
        pet.group.add(group)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(instance=pet)
        return Response(data=serializer.data, status=200)
