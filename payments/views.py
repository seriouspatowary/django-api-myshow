from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import create_order,verify_payment,get_myorders
from common.authentication import JWTAuthentication

class CreateOrderAPIView(APIView):

    def post(self, request):
        try:
            result = create_order(request.data)

            return Response(
                {
                    "success": True,
                    "data": result
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
            
class VerifyPaymentAPIView(APIView):

    def post(self, request):
        try:
            result = verify_payment(request.data)

            return Response(
                {
                    "success": True,
                    "data": result
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

class MyOrderAPIView(APIView):
    authentication_classes =[JWTAuthentication]
     
    def get(self, request):
        try:
            result = get_myorders(request.user["_id"])

            return Response(
                {
                    "success": True,
                    "data": result
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
