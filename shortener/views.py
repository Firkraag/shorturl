from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import View

from analytics.models import ClickEvent
from .forms import SubmitUrlForm
from .models import ShortURL


# Create your views here.
class URLRedirectView(View):
    def get(self, request, shortcode):
        obj = get_object_or_404(ShortURL, shortcode=shortcode)
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)


class HomeView(View):
    def get(self, request):
        context = {
            "form": SubmitUrlForm(),
        }
        return render(request, "shortener/home.html", context)

    def post(self, request: HttpRequest):
        form = SubmitUrlForm(request.POST)
        context = {
            "form": form,
        }
        template = "shortener/home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get('url')
            obj, created = ShortURL.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
            }
            template = "shortener/shortener.html"
        return render(request, template, context)
