from django.urls import reverse
from django.shortcuts import redirect
class RedirectAuthenticatedUserMiddleWare:
    def __init__(self,get_response):
        self.get_response= get_response
    def __call__(self, request):
        # check the user is authenticated
        if request.user.is_authenticated:
            # list of path to check
            path_to_redirect=[reverse('blog:login'),reverse('blog:register')]
            if request.path in path_to_redirect:
                return redirect(reverse('blog:index')) #change lane to index home page
        response= self.get_response(request)
        return response




class RestrictUnauthenticatedUserMiddleWare:
    def __init__(self,get_response):
        self.get_response= get_response
    def __call__(self, request):
        restricred_paths=[reverse('blog:dashboard')]

        if not request.user.is_authenticated and request.path in restricred_paths:
            return redirect(reverse('blog:login'))
        response=self.get_response(request)
        return response