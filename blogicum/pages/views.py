from django.shortcuts import render


def permission_denied(request, exception):
    template_name = 'pages/403csrf.html'
    return render(request, template_name, status=403)


def page_not_found(request, exception):
    template_name = 'pages/404.html'
    return render(request, template_name, status=404)


def server_error(request):
    template_name = 'pages/500.html'
    return render(request, template_name, status=500)
