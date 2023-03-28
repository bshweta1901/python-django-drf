# from django.shortcuts import render
from .models import Brands,Products,Variants
from rest_framework import viewsets
from .serializer import Multipleimageserializer
from .serializer import Multipleimageserializer,ProductfirstSerializer,ProductDetailsSerializers
from rest_framework.decorators import action
# from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.viewsets import GenericViewSet
# from rest_framework.decorators import action
# from rest_framework.mixins import CreateModelMixin
# from django.shortcuts import get_object_or_/404
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

# Create your views here.

#Add Multiple Images
class MultipleimageViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = Multipleimageserializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_brand']


    parser_classes = (MultiPartParser, FormParser)


#Display the Product
class Productviewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductfirstSerializer



class ProductDetailsviewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductDetailsSerializers
    filter_backends = [DjangoFilterBackend]
    # filterset_class = ProductFilter
    # def retrieve(self, request, *args, **kwargs):
    #     size_name = request.query_params.get('size')
    #     kwargs['context'] = {'size_name': size_name}
    #     return super().retrieve(request, *args, **kwargs)
    