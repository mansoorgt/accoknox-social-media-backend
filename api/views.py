from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
import json
from django.core.paginator import Paginator
from django.db.models import Q
from api.models import *
from itertools import chain
# Create your views here.
class LogOutView(APIView):
    pass

class SignUpView(CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)

class LoginView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer
    def post(self,request):
        serializer=SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)

        return Response({
            "status":"success",
            "token":token.key
        }, status=status.HTTP_200_OK)

class UserSearch(APIView):
    
    permission_classes=[IsAuthenticated]
    serializer_class = UsersSerializer
    def get(self,request):
        search_value=request.data.get('search-value')
        per_page_count=request.data.get('count')
        page=request.data.get('page')
        if not search_value:
            return Response({"message":"search-value field is required","status":"error"})
        searched_results=User.objects.filter(Q(username__icontains=search_value) | Q(first_name__icontains=search_value) | Q(last_name__icontains=search_value))
        
        paginator=Paginator(searched_results,per_page_count)
        page_obj=paginator.get_page(page)
        serializer=UsersSerializer(data=page_obj,many=True)
        serializer.is_valid()
       
        return Response({"result":serializer.data,"pagination":{
            "has_next":page_obj.has_next(),
            "has_previous":page_obj.has_previous(),
            "total_result":searched_results.count(),
            "current_page":page_obj.number
            
        }})

class SendFriendRequest(CreateAPIView):
    permission_classes=[IsAuthenticated]
    
    def create(self,request):
        
        receiver_email=request.data.get("receiver-email")
        receiver=User.objects.get(email=receiver_email)
        
        if Friends.objects.filter(sender=request.user,receiver=receiver,request_status=0).exists():
            return Response({"status":"error","message":'pending request already exist'})
        
        #setup time limit
        # if Friends.objects.filter(sender=request.user,request_status=0,created_at__=)
        
        Friends.objects.create(sender=request.user,receiver=receiver,request_status=0)
        
        return Response({"status":"success"})

class UpdateFriendRequest(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        request_status=request.data.get('request-status')
        sender_email=request.data.get('sender-email')

        if not Friends.objects.filter(receiver=request.user,request_status=0).filter(sender__email=sender_email).exists():
            return Response({"status":"error","message":"Friend request not in pending or friend request not exist"})
        
        if request_status == 'accept':
            Friends.objects.filter(receiver=request.user,sender__email=sender_email).update(request_status=1)

        elif request_status == 'reject':
            Friends.objects.filter(receiver=request.user,sender__email=sender_email).update(request_status=2)
        else:
            return Response({"status":"error","message":"request-status not valid please input accept/reject"})
            
        return Response({"status":"success",})
class GetPendingFriendRequest(APIView):
    
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        pendingFriendRequests=Friends.objects.filter(receiver=request.user,request_status=0).values_list("sender__id",flat=True)
        
        
        serializer=UsersSerializer(data=User.objects.filter(id__in=pendingFriendRequests),many=True)
        serializer.is_valid()
        
        return Response({
            'results':serializer.data
        })
        
class GetAllFriends(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        
        friends_senders=Friends.objects.filter(Q(receiver=request.user)|Q(sender=request.user)).filter(request_status=1).values_list("sender__id",flat=True)
        friends_receivers=Friends.objects.filter(Q(receiver=request.user)|Q(sender=request.user)).filter(request_status=1).values_list("receiver__id",flat=True)
        
        
        serializer=UsersSerializer(data=User.objects.filter(id__in=chain(friends_receivers,friends_senders)).exclude(id=request.user.id),many=True)
        serializer.is_valid()
        
        return Response({
            'results':serializer.data
        })      
        