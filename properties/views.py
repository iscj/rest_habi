from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import  JsonResponse

from .models import PropertyModel

@api_view(['POST'])
def property_filter(request):
    if request.method == 'POST':
        filters = request.data
        property = PropertyModel()
        results = property.filters(filters)
        if results is None:
            JsonResponse.status_code = 405
            return JsonResponse({"detail": "Error with params"})
        
        return JsonResponse({'inmuebles': results},  safe=False)

@api_view(['POST'])
def property_available(request):
    if request.method == 'POST':
        property = PropertyModel()
        results = property.last_status()
        if results is None:
            JsonResponse.status_code = 405
            return JsonResponse({"detail": "Error with params"})
            
        return JsonResponse({'inmuebles': results},  safe=False)
