from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import get_movies, create_movie, delete_movie, update_movie
from common.authentication import JWTAuthentication
from common.permissions import IsAdmin


class UpdateMovieAPIView(APIView):

    authentication_classes =[JWTAuthentication]
    permission_classes = [IsAdmin]

    def put(self,request,id):
        try:
            movie = update_movie(id, request.data)

            return Response(
                {
                    "success": True,
                    "message":"Movie Updated Successfully",
                    "data": movie
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
        



class deleteMovieAPIView(APIView):
    authentication_classes =[JWTAuthentication]
    permission_classes= [IsAdmin]

    def delete(self, request, id):
        try:
            delete_movie(id)

           
            return Response(
                {
                    "success": True,
                    "message": "Movie deleted successfully"
                },
                status=status.HTTP_200_OK
            )


        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )



class CreatedAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def post(self,request):
        try:
            movie = create_movie(request.data)

            return Response(
                {
                    "success":True,
                    "message": "Movie Created Successfully",
                    "movie":movie
                                    
                },

                status = status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                    {
                     
                     "success":False,
                     "message": str(e)
                 
                      },
                      
                      status = status.HTTP_400_BAD_REQUEST
                      
                    )





class MovieListAPIView(APIView):

    def get(self,request):

        try:
            movies = get_movies()

            return Response(
                {
                     "success": True,
                     "data": movies
                },
              status = status.HTTP_200_OK
            )

        except Exception as e:
            return  Response({
                "success":False,
                "message":str(e)

            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        
            )
