from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import get_movies, create_movie, delete_movie, update_movie, get_display_movies,get_public_movies,create_movie_cast, create_movie_crew, get_movie_cast_by_movieId, get_movie_crew_by_movieId, get_movie_by_movieId
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
            movie = create_movie(request.data,request.user["_id"])

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




class PublicMovieListAPIView(APIView):

    def get(self, request):
        movies = get_public_movies()

        return Response(
            {
                "success": True,
                "movies": movies
            },
            status=status.HTTP_200_OK
        )


class displaynameAPIView(APIView):
      def get(self, request):
        movies = get_display_movies()

        return Response(
            {
                "success": True,
                "movies": movies
            },
            status=status.HTTP_200_OK
        )



class MovieListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request):
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 10)

        data = get_movies(
            request.user["_id"],
            page,
            limit
        )

        return Response(
            {
                "success": True,
                "data": data
            }
        )
    

class castAddAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    
    def post(self,request):
        try:
            movie = create_movie_cast(request.data)

            return Response(
                {
                    "success":True,
                    "message": "Movie Cast Created Successfully",
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



class MovieCastDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, movieId):
        try:
            cast = get_movie_cast_by_movieId(movieId)

            return Response(
                {
                    "success": True,
                    "cast": cast,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_404_NOT_FOUND,
            )
            
            
class crewAddAPIView(APIView):
     authentication_classes = [JWTAuthentication]
     permission_classes = [IsAdmin]
     
     def post(self, request):
          try:
            movie = create_movie_crew(request.data)

            return Response(
                {
                    "success":True,
                    "message": "Movie Crew Created Successfully",
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


class  MovieCrewDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, movieId):
        try:
            crew = get_movie_crew_by_movieId(movieId)

            return Response(
                {
                    "success": True,
                    "crew": crew,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_404_NOT_FOUND,
            )
            
            


class MovieByIdAPIView(APIView):
      
      def get(self,request,id):
            try:
              
              movie = get_movie_by_movieId(id)
              
              return Response(
                  {
                    "success":True,
                    "movie": movie
                  },
                  status = status.HTTP_200_OK
                  
              )
            except Exception as e:
                return Response(
                    {
                         "success": False,
                         "message":str(e)
                    },
                    status = status.HTTP_404_NOT_FOUND,
                )