from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import register_user, login_user, refresh_access_token
import os

is_production = os.getenv("ENVIRONMENT") == "production"

class LogoutAPIView(APIView):

    def post(self, request):

        response = Response(
            {
                "success": True,
                "message": "Logged out successfully"
            },
            status=status.HTTP_200_OK
        )

        response.delete_cookie("refreshToken")

        return response


class RefreshTokenAPIView(APIView):

    def post(slef,request):
        try:
            refresh_token = request.COOKIES.get(
                "refreshToken"
            )
        

            if not refresh_token:
                return Response({
                      "success": False,
                      "message": "Refresh Token Missing"
                    },
                       status=status.HTTP_401_UNAUTHORIZED
                    )
            
            result = refresh_access_token(refresh_token)


            return Response({
                "success": True,
                "accessToken":result["access_token"],
                "user":result["user"]

            },
            
            )
            
        except Exception:
             return Response({
                 "success": False,
                 "message": "Invalifd Refresh Token",

                 },
                 status = status.HTTP_401_UNAUTHORIZED
                    
                    
                )
        



class RegisterAPIView(APIView):

    def post(self, request):
        try:
            user = register_user(request.data)

            user.pop("password", None)

            return Response(
                {
                    "success": True,
                    "message": "Registration successful",
                    "user": user,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginAPIView(APIView):

    def post(self, request):
        try:
            result = login_user(request.data)

            # print(f"result is {result}")

            response = Response(
                {
                    "success": True,
                    "message": "Login successful",
                    "accessToken": result["access_token"],
                    "user": result["user"],
                },
                status=status.HTTP_200_OK,
            )

            if is_production:
                    response.set_cookie(
                        key="refreshToken",
                        value=result["refresh_token"],
                        httponly=True,
                        secure=is_production,     # Change to True in production (HTTPS)
                        samesite="None",    # Use "None" for cross-site HTTPS
                        max_age=30 * 24 * 60 * 60,
                    )
            else:
                response.set_cookie(
                    key="refreshToken",
                    value=result["refresh_token"],
                    httponly=True,
                    secure=False,
                    samesite="Lax",
                    max_age=30 * 24 * 60 * 60,
                )

            return response

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e),
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )