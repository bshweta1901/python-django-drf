from rest_framework import serializers
from .models import Products,Color,Size,Brands,Imaget, Variants
from importlib.resources import read_binary
from itertools import product
from django.db import transaction

#product_name,brand_name,Price,default_image

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brands
        fields =['brand_title']

class ProductfirstSerializer(serializers.ModelSerializer):
    product_brand = BrandSerializer(read_only=True)
    default_image = serializers.SerializerMethodField()
    # variant =  ProductVariantSerializer(many=True, read_only=True,source='variants'  )
    read_only_fields = ('variant',)
    class Meta:
        model = Products
        fields = ["product_name","default_image","product_brand"]


    def get_default_image(self, obj):
        default_image = obj.images.filter(is_default=True).first()
        if default_image:
            return default_image.image.url
        return None



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True)
    size = SizeSerializer()
    color = ColorSerializer()

    class Meta:
        model = Variants
        fields = ['id', 'product', 'size', 'color', 'price']

   

#details

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True)
    size = SizeSerializer()
    color = ColorSerializer()

    class Meta:
        model = Variants
        fields = ['id', 'product', 'size', 'color', 'price']
    

#filter the product by size and color

class ProductDetailsSerializers(serializers.ModelSerializer):  
    #  images =  ProductImageSerializer(many=True, read_only=True)  
     variants =  ProductVariantSerializer(many=True, read_only=True  )
     read_only_fields = ('variant',)
    #  size =  SizeSerializer(many=True, read_only=True)  
     class Meta:
        model = Products
        #fields=('firstname','lastname')
        fields = [ "product_name","product_brand","price",'variants']
     def to_representation(self, instance):
        # Get the size and color from the request query parameters
        size_code = self.context['request'].query_params.get('size')
        color_id = self.context['request'].query_params.get('color_id')
        print("SIZE+++++++++++++++++++++++++++",size_code)

        # Filter the variants based on the specified size and color
        if size_code and color_id:
            variants = instance.variants.filter(size__code=size_code, color__id=color_id)
        elif size_code:
            variants = instance.variants.filter(size__code=size_code)
        elif color_id:
            variants = instance.variants.filter(color__id=color_id)
        else:
            variants = instance.variants.all()

        # Serialize only the variants that match the specified size and color
        variants_data = ProductVariantSerializer(variants, many=True).data

        # Return the modified representation
        return {
            'product_name': instance.product_name,
            'product_brand': instance.product_brand.id,
            'price': instance.price,
            'variants': variants_data
        }
        












class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imaget
        fields = ['image']


class Multipleimageserializer(serializers.ModelSerializer):
    images =  ProductImageSerializer(many=True, read_only=True)
    defaultimage = ProductImageSerializer(read_only=True, source='get_default_image')
    # variants = ProductVariantSerializer(read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True)
    default_image = serializers.PrimaryKeyRelatedField(queryset=Imaget.objects.all(), required=False)
    class Meta:
        model = Products
        fields = [ "id" ,"product_name","product_brand","price", "images","default_image", "uploaded_images","defaultimage"]
        read_only_fields = ('default_image',)
    
    
    def create(self, validated_data):
        images_data = validated_data.pop("uploaded_images",[])
        product = Products.objects.create(**validated_data)
        default_image = None
        with transaction.atomic():
            for i, image_data in enumerate(images_data):
                is_default = self.initial_data.get(f'images[{i}][is_default]', False)
                # is_default = image_data.get('is_default', False)
                image = Imaget.objects.create(product=product, image=image_data, is_default=is_default)
                print("IMAGE",image)
                if is_default:
                    default_image = image
                        
            if not default_image and images_data:
                default_image = product.images.first()
                is_default=default_image
                print(is_default)
                
            if default_image:
               
                product.default_image = default_image
                product.default_image.is_default = True
                product.default_image.save()
                product.save()
        return product


















'''
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True)
    size = SizeSerializer()
    color = ColorSerializer()

    class Meta:
        model = Variants
        fields = ['id', 'product', 'size', 'color', 'price']



class ProductDetailsSerializers(serializers.ModelSerializer):  
    #  images =  ProductImageSerializer(many=True, read_only=True)  
     variant =  ProductVariantSerializer(many=True, read_only=True,source='variants'  )
     read_only_fields = ('variant',)
    #  size =  SizeSerializer(many=True, read_only=True)  
     class Meta:
        model = Products
        #fields=('firstname','lastname')
        fields = [ "product_name","product_brand","price",'variant']





class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imaget
        fields = ['image']


class Multipleimageserializer(serializers.ModelSerializer):
    images =  ProductImageSerializer(many=True, read_only=True)
    defaultimage = ProductImageSerializer(read_only=True, source='get_default_image')
    # variants = ProductVariantSerializer(read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True)
    default_image = serializers.PrimaryKeyRelatedField(queryset=Imaget.objects.all(), required=False)
    class Meta:
        model = Products
        fields = [ "id" ,"product_name","product_brand","price", "images","default_image", "uploaded_images","defaultimage"]
        read_only_fields = ('default_image',)
    
    
    def create(self, validated_data):
        images_data = validated_data.pop("uploaded_images",[])
        product = Products.objects.create(**validated_data)
        default_image = None
        with transaction.atomic():
            for i, image_data in enumerate(images_data):
                is_default = self.initial_data.get(f'images[{i}][is_default]', False)
                # is_default = image_data.get('is_default', False)
                image = Imaget.objects.create(product=product, image=image_data, is_default=is_default)
                print("IMAGE",image)
                if is_default:
                    default_image = image
                        
            if not default_image and images_data:
                default_image = product.images.first()
                is_default=default_image
                print(is_default)
                
            if default_image:
               
                product.default_image = default_image
                product.default_image.is_default = True
                product.default_image.save()
                product.save()
        return product








'''
































# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Imaget
#         fields = ('id', 'image', 'is_default')

class ProductSerializer(serializers.ModelSerializer):
    default_image = serializers.SerializerMethodField()

    def get_default_image(self, obj):
        default_image = obj.images.filter(is_default=True).first()
        if default_image:
            return default_image.image.url
        return None

    class Meta:
        model = Products
        fields = (  "product_name","product_brand", 'default_image')
