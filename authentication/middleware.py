from django.conf import settings
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    """
    Middleware para exigir autenticação em todas as rotas, exceto as especificadas
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Rotas que não exigem autenticação
        self.exempt_urls = [
            '/authentication/login/',
            '/authentication/register/',
            '/authentication/logout/',
            '/admin/login/',
            '/admin/'
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if path not in self.exempt_urls and not path.startswith('/static/'):
                return redirect(settings.LOGIN_URL + '?next=' + path)
        
        response = self.get_response(request)
        return response
