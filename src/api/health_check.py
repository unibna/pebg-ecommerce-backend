from django.http import JsonResponse

from django.core.cache import cache


def health_check(request):
  return JsonResponse({"status": "ok"})
