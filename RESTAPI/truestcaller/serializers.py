from django.db import transaction

from rest_framework import serializers

from truestcaller import (
    models as truestcaller_models,
    utils as truestcaller_utils
)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = truestcaller_models.User
        fields = ('name', 'phone_number', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    @transaction.atomic()
    def create(self, validated_data):
        user = truestcaller_models.User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        del validated_data['email']
        del validated_data['password']
        validated_data['added_by'] = user
        truestcaller_models.Directory.objects.create(**validated_data)
        truestcaller_utils.add_user_contact_book(user)
        return user


class PhoneNumberSpamSerializer(serializers.ModelSerializer):

    class Meta:
        model = truestcaller_models.Directory
        fields = ('phone_number', 'is_spam')


class CustomSearchSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_null=True)

    class Meta:
        model = truestcaller_models.Directory
        fields = ('name', 'phone_number', 'is_spam', 'email')
