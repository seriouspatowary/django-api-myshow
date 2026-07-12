from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import get_movies



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
