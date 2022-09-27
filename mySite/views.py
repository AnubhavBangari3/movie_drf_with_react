
from os import stat
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .models import Movie,Like,DisLike
from.serializers import UserSerializer,MovieSerializer,LikeSerializer,DisLikeSerializer

from django.db.models import Q

import pandas as pd
from django.http import HttpResponse
from rest_framework.generics import ListAPIView

from collections import defaultdict
#------------------------------------------------------------------------------------------

class UserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
class MovieViewset(viewsets.ModelViewSet):
    
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    
class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    def get(self, request):
        #Need to change this
        #request.user.auth_token.delete() wrong
        token=request.user.auth_token
        #print(token.user.id)
        return Response(status=status.HTTP_200_OK)
    
class getCurrentUser(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user=User.objects.get(username=self.request.user)
        token_ex=Token.objects.get(user=user)
        #print(token_ex)
        serializer=UserSerializer(user)
        #print(user,serializer)
        return Response(serializer.data)
#------------------------------------------------------------------------------------------------------------------

'''
Now 
in like view I need to add this logic
1) If post has 0 dislike, then we like it -> It should show 1 like
2)If post has 1 or more dislike, then we like it -> dislike count shoild decrease by 1 and like should increase by 1
'''

class likeMovie(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    serializer_class=LikeSerializer
    
    def post(self,request,pk):
        #This view will be used for liking the movie
        #It has two foreign keys 1)User, 2) Movie
        
        #user,movie
        user_liking_this_movie=User.objects.get(username=self.request.user)
        movie_liked_by_this_user=get_object_or_404(Movie,pk=pk)
        #print("Like movie view {} {}".format(user_liking_this_movie,movie_liked_by_this_user))
        
        serializer=LikeSerializer(data=request.data)
        #Delete if user has already liked
        if user_liking_this_movie in movie_liked_by_this_user.like.all():
            movie_liked_by_this_user.like.remove(user_liking_this_movie)
        #If moiveis laready disliked, then user like it-> dislike decrease by 1 and like increase by 1
        elif user_liking_this_movie in movie_liked_by_this_user.unlike.all():
            movie_liked_by_this_user.unlike.remove(user_liking_this_movie)
            movie_liked_by_this_user.like.add(user_liking_this_movie)
        
        else:
            #Like it
            movie_liked_by_this_user.like.add(user_liking_this_movie)
        #CHecking if this movie is liked by the user
        check=Like.objects.filter(Q(userL=user_liking_this_movie) & Q(movieL=movie_liked_by_this_user))
        
        if(check.exists()):
            #if already liked then delete the like
            check.delete()
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message":"Already Liked"
            })
        #Create new like
        new_like=Like.objects.create(userL=user_liking_this_movie,movieL=movie_liked_by_this_user)
        
        new_like.save()
        serializer=LikeSerializer(new_like)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class dislikeMovie(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    serializer_class=DisLikeSerializer
    
    def post(self,request,pk):
        #This view will be used for disliking the movie
        #It has two foreign keys 1)User, 2) Movie
        
        #user,movie
        user_disliking_this_movie=User.objects.get(username=self.request.user)
        movie_disliked_by_this_user=get_object_or_404(Movie,pk=pk)
        
        serializer=DisLikeSerializer(data=request.data)
        #Delete if user has already disliked
        if user_disliking_this_movie in movie_disliked_by_this_user.unlike.all():
            movie_disliked_by_this_user.unlike.remove(user_disliking_this_movie)
            
        elif user_disliking_this_movie in movie_disliked_by_this_user.like.all():
            movie_disliked_by_this_user.like.remove(user_disliking_this_movie)
            movie_disliked_by_this_user.unlike.add(user_disliking_this_movie)
        
        else:
            #DisLike it
            movie_disliked_by_this_user.unlike.add(user_disliking_this_movie)
        #CHecking if this movie is liked by the user
        check=DisLike.objects.filter(Q(userDL=user_disliking_this_movie) & Q(movieDL=movie_disliked_by_this_user))
        
        if(check.exists()):
            #if already disliked then delete the like
            check.delete()
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message":"Already DisLiked"
            })
        #Create new dislike
        new_dislike=DisLike.objects.create(userDL=user_disliking_this_movie,movieDL=movie_disliked_by_this_user)
        
        new_dislike.save()
        serializer=DisLikeSerializer(new_dislike)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
#------------------------------------------------------------------------------------------------------------------


class PersonalizedView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        
        user=User.objects.get(username=self.request.user)
        movies=Movie.objects.filter(like=user.id)
        print(f"User - {user} movies - {movies}")
        serializer=MovieSerializer(movies,many=True)
        #print(serializer.data)
        
        return Response(serializer.data)

class ReommendView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    serializer_class=MovieSerializer
    def get(self,request):
        movie=Movie.objects.all().values()
        #All movie dataframe
        pd_movie=pd.DataFrame(movie)
        
        l=Movie.objects.filter(like=User.objects.get(username=self.request.user)).values()
        #Movie liked by the current user dataframe
        pd_liked_movie=pd.DataFrame(l)
        #print(pd_liked_movie)
        movie_genre={}
        for i in pd_liked_movie.index:
            
            movie_genre[pd_liked_movie['title'][i]]=pd_liked_movie['genre'][i]
        #Genre cur liked
        cur_max={}
        
        for i in movie_genre.values():
            if i in cur_max:
                cur_max[i]+=1
            else:
                cur_max[i]=1
                
        #Defaultdict for genre like count        
        recommendations=defaultdict(list)
        for key, value in cur_max.items():
            recommendations[value].append(key)
        #print(recommendations)
        
        #Highest genre of movie liked
        recommend=list(max(recommendations.items())[1])
        #print(recommend)
        result=[]
        for i in recommend:
            moviereturn=Movie.objects.filter(Q(genre=i))
            #print(moviereturn,i)
            serializer=MovieSerializer(moviereturn,many=True)
            result.append(serializer.data)
        print(result)
            
        return Response(serializer.data)
        

    