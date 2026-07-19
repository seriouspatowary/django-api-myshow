from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from common.authentication import JWTAuthentication
from common.permissions import IsAdmin
from .services import create_theatre,get_theatre,update_theatre, delete_theatre, create_screen


# Create your views here.

class GetThetreAPIView(APIView):
    def get(self, request):
        try:
        
            page = request.GET.get("page", 1)
            limit = request.GET.get("limit", 10)
            search = request.GET.get("search","")

            data  = get_theatre(page,limit)
            
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
        
        
        
        
        