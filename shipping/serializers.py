from rest_framework import serializers
from .models import Shipping

class ShippingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'name', 'phone', 'email', 'state', 'city', 'thana', 'note', 'detail_address', 'is_default', 'address_type']

        extra_kwargs = {
            'id': {'read_only': True},
            'state': {'required': True, 'allow_null': False},
            'city': {'required': True, 'allow_null': False},
            'thana': {'required': True, 'allow_null': False},
            'detail_address': {'required': True, 'allow_null': False},
            'note': {'required': False, 'allow_null': True},
            'is_default': {'required': False, 'allow_null': True},
            'name': {'required': True, 'allow_null': False},
            'phone': {'required': True, 'allow_null': False},
            'email': {'required': False, 'allow_null': True},
            'address_type': {'required': True, 'allow_null': False},
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        # Rest of them would be false
        if validated_data.get('is_default'):
            Shipping.objects.filter(user=validated_data['user']).update(is_default=False)

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if validated_data.get('is_default'):
            Shipping.objects.filter(user=instance.user).update(is_default=False)

        return super().update(instance, validated_data)

class ShippingReadSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    thana = serializers.SerializerMethodField()
    
    class Meta:
        model = Shipping
        fields = ['id', 'name', 'phone', 'email', 'state', 'city', 'thana', 'detail_address', 'note', 'is_default', 'address_type']

    def get_state(self, obj):
        return {
            "id": obj.state.id,
            "name": obj.state.name,
            "name_bn": obj.state.name_bn,
        }

    def get_city(self, obj):
        return {
            "id": obj.city.id,
            "name": obj.city.name,
            "name_bn": obj.city.name_bn,
        }

    def get_thana(self, obj):
        return {
            "id": obj.thana.id,
            "name": obj.thana.name,
            "name_bn": obj.thana.name_bn,
        }

