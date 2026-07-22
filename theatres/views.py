from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.authentication import JWTAuthentication
from common.permissions import IsAdmin
from .services import create_theatre,get_theatre,update_theatre, delete_theatre, create_screen, get_theatre_list,get_theatre_screen_list,create_seat_layout,get_seat_list, get_seat_type


# Create your views here.

class GetThetreAPIView(APIView):
    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAdmin]
    
    
    def get(self, request):
        try:
        
            page = request.GET.get("page", 1)
            limit = request.GET.get("limit", 10)
            search = request.GET.get("search","")

            data  = get_theatre(page,limit,request.user["_id"],search)
            
            return Response(
                {
                    "success":True,
                     "data": data
                    
                },
                status= status.HTTP_200_OK
            )
            
        except Exception as e:
            
            return Response(
                {
                     "success":False,
                     "message":str(e)
                },
                status= status.HTTP_400_BAD_REQUEST
            )
            
        


class AddTheatreAPIView(APIView):
    
    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAdmin]
    
    def post(self,request):
       try:
                theatre = create_theatre(request.data)
               
                return Response(
                    {
                         "success":True,
                         "message":"Theatre Created Successfully",
                        #   theatre: theatre
                        
                    },
                    status = status.HTTP_200_OK
                )
        
       except Exception as e:
        
                return Response(
                    {
                        "success":False,
                        "message":str(e)
                        
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

class UpdateAPIView(APIView):
    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAdmin]
    
    def put(self,request,id):
       try:
                theatre = update_theatre(id, request.data)
               
                return Response(
                    {
                         "success":True,
                         "message":"Theatre Updated Successfully",
                        #   theatre: theatre
                        
                    },
                    status = status.HTTP_200_OK
                )
        
       except Exception as e:
        
                return Response(
                    {
                        "success":False,
                        "message":str(e)
                        
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
                
class  DeleteAPIView(APIView):
    
    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAdmin]
    
    def delete(self,request,id):
       try:
                delete_theatre(id)
               
                return Response(
                    {
                         "success":True,
                         "message":"Theatre Deleted Successfully",
                        #   theatre: theatre
                        
                    },
                    status = status.HTTP_200_OK
                )
        
       except Exception as e:
        
                return Response(
                    {
                        "success":False,
                        "message":str(e)
                        
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )


class AddScreenAPIView(APIView):
    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAdmin]
    
    def post(self,request):
       try: 
           screen = create_screen(request.data)
           
           
           return Response(
               {
                   "success":True,
                    "message":"Screen Created Successfully",
                    "data":screen
               },
               status= status.HTTP_200_OK
               
           )
           
           
           
       except Exception as e:
           return Response(
               {
                    "success":False,
                    "message":str(e)
               },
               status= status.HTTP_400_BAD_REQUEST
            )
        
class TheatreListAPIView(APIView):
    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAdmin]
    
    def get(self, request):
        try:
            
            print("userId:",request.user["_id"])

            data  = get_theatre_list(request.user["_id"])
            
            return Response(
                {
                     "success":True,
                     "data": data
                    
                },
                status= status.HTTP_200_OK
            )
            
        except Exception as e:
            
            return Response(
                {
                     "success":False,
                     "message":str(e)
                },
                status= status.HTTP_400_BAD_REQUEST
            )
            
    
        
class screenListAPIView(APIView):
    
     def get(self, request, id):
        try:

            data  = get_theatre_screen_list(id)
            
            return Response(
                {
                    "success":True,
                     "data": data
                    
                },
                status= status.HTTP_200_OK
            )
            
        except Exception as e:
            
            return Response(
                {
                     "success":False,
                     "message":str(e)
                },
                status= status.HTTP_400_BAD_REQUEST
            )
            
class  SeatsAddAPIView(APIView):
    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAdmin]
    
    def post(self,request):
       try: 
           layout = create_seat_layout(request.data, request.user["_id"])
           
           
           return Response(
               {
                   "success":True,
                    "message":"Layout Created Successfully"
               },
               status= status.HTTP_200_OK
               
           )
           
       except Exception as e:
           return Response(
               {
                    "success":False,
                    "message":str(e)
               },
               status= status.HTTP_400_BAD_REQUEST
            )
           
class GetSeatLayoutAPIView(APIView):
    
     def get(self, request, id):
        try:

            data  = get_seat_list(id)
            
            return Response(
                {
                    "success":True,
                     "data": data
                    
                },
                status= status.HTTP_200_OK
            )
            
        except Exception as e:
            
            return Response(
                {
                     "success":False,
                     "message":str(e)
                },
                status= status.HTTP_400_BAD_REQUEST
                
            )
            
            
class GetSeatTypeAPIView(APIView):
     def get(self, request, id):
        try:

            data  = get_seat_type(id)
            
            return Response(
                {
                    "success":True,
                     "data": data
                    
                },
                status= status.HTTP_200_OK
            )
            
        except Exception as e:
            
            return Response(
                {
                     "success":False,
                     "message":str(e)
                },
                status= status.HTTP_400_BAD_REQUEST
                
            )