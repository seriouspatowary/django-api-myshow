from rest_framework.views import APIView
from rest_framework.response import Response

class StudentAPIView(APIView):
    def get(self, request):
        return Response({
            "success": True,
            "message": "Student API is working!"
        })