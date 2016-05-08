from django.shortcuts import render

class RerouteMiddleware:
    def process_request(request):
	if not request.is_ajax(): 
	    return render(request, 'ausome_sports/index.html')
        return None
