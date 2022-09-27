from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from .models import Movie,Like,DisLike


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password']
        
        extra_kwargs={
            'password':{
                'write_only':True,'required':True
            }
            
        }
        def create(self,validated_data):
            user=User.objects.create(**validated_data)
            
            token=Token.objects.create(user=user)
            #print(user,token)
            return user

class MovieSerializer(serializers.ModelSerializer):
    total_likes=serializers.SerializerMethodField()
    total_dislikes=serializers.SerializerMethodField()
    class Meta:
        model=Movie
        fields=('id','title','director','stars','genre','like','unlike','total_likes','total_dislikes',)
    def get_total_likes(self,instance):
        return instance.like.all().count()
    def get_total_dislikes(self,instance):
        return instance.unlike.all().count()
        

class LikeSerializer(serializers.ModelSerializer):
    userL=serializers.PrimaryKeyRelatedField(read_only=True)
    movieL=serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model=Like
        fields=('id','userL','movieL',)
        
class DisLikeSerializer(serializers.ModelSerializer):
    userDL=serializers.PrimaryKeyRelatedField(read_only=True)
    movieDL=serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model=DisLike
        fields=('id','userDL','movieDL',)
        

# class PersonalizedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Movie
#         fields=('id','title','genre','like',)