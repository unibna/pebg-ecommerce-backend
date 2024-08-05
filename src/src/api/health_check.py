from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


def health_check(request):
    return JsonResponse({"status": "ok"})


class TestAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        value = request.user.departments.first()
        return JsonResponse({
            "data": f"{value}"
        })
