from wsgiref import validate
from .models import User, Student, Post
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Student.objects.create(
            user = user,
            batch = self.initial_data.get('batch'),
            specialization = self.initial_data.get('specialization'),
            profile = self.initial_data.get('profile')
        )
        return user
    
    # def update(self, instance, validated_data):
    #     instance.role = validated_data.get('role')
    #     instance.save()
    #     return instance

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['is_staff'] = False
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'