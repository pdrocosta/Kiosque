from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Pet
from .serializers import PetSerializer
from traits.models import Trait
from groups.models import Group
from rest_framework.pagination import PageNumberPagination


class PetsView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        query_trait = request.query_params.get("trait")
        if query_trait:
            pets = Pet.objects.filter(
                traits__name__iexact=query_trait
            )
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        traits_data = serializer.validated_data.pop("traits")
        group_data = serializer.validated_data.pop("group")

        group_exist = Group.objects.get_or_create(
            group_data
        )
        pet = Pet.objects.create(**serializer.validated_data,
                                 group=group_exist[0])
        for trait in traits_data:
            traits_exist = Trait.objects.filter(name__iexact=trait["name"])
            pet.traits.add(traits_exist.first())
            if not traits_exist:
                traits_exist = Trait.objects.create(**trait)
                pet.traits.add(traits_exist)
        serializer = PetSerializer(pet)
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
            serializer = PetSerializer(instance=pet, data=request.data,
                                       partial=True)
            serializer.is_valid(raise_exception=True)
        except ObjectDoesNotExist:
            return Response(data={"detail": "Not found."}, status=404)

        traits_data = serializer.validated_data.pop("traits", None)
        group_data = serializer.validated_data.pop("group", None)
        pet_name = serializer.validated_data.get("name", None)

        if traits_data:
            for trait in traits_data:
                trait_data = Trait.objects.get_or_create(
                    trait_name__iexact=trait["trait_name"],
                    defaults=trait)
            pet.traits.add(trait_data)

        if group_data:
            group = Group.objects.get_or_create(
                scientific_name__iexact=group["scientific_name"],
                defaults=group)
            pet.group.add(group)

        if pet_name:
            name = Pet.objects.get_or_create(
                name__iexact=pet["name"],
                defaults=name)
            pet.name.append(name)
        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(instance=pet)
        return Response(data=serializer.data, status=200)
