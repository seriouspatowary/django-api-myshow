from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import create_show, get_shows, update_show, get_show_byId
from common.authentication import JWTAuthentication
from common.permissions import IsAdmin

 
class ShowListAPIView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    
    def get(self, request):
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 10)

        data = get_shows(
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
    

    
 
    

class AddShowPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def post(self,request):
        try:
            shows = create_show(request.data,request.user["_id"])

            return Response(
                {
                    "success":True,
                    "message": "Show Created Successfully",
                    "data":shows
                                    
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


class EditShowAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def patch(self, request, showId):
        try:
            show = update_show(
                request.data,
                showId,
                request.user["_id"]
            )

            return Response(
                {
                    "success": True,
                    "message": "Show updated successfully",
                    "data": show
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
            
class GetShowByIdAPIView(APIView):
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdmin]

    def get(self, request, showId):
        try:
            show = get_show_byId(
                showId
            )

            return Response(
                {
                    "success": True,
                    "data": show
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
            