import datetime
from threading import Thread

from rest_framework import viewsets
from django.http import HttpResponse

from ginkgo.serializers import BlastQuerySerializer, BlastResultSerializer
from ginkgo.models import BlastQuery, BlastResult
from ginkgo.utils import process_query


# Create your views here.
class BlastQueryViewSet(viewsets.ModelViewSet):
    queryset = BlastQuery.objects.all()
    serializer_class = BlastQuerySerializer

    def get_queryset(self):
        user_cookie = self.request.query_params.get("user_cookie", None)
        qs = BlastQuery.objects.all()
        if user_cookie:
            qs = qs.filter(user_cookie=user_cookie)
        dna_seq = self.request.query_params.get("dna_sequence", None)
        if dna_seq:
            qs = qs.filter(dna_sequence=dna_seq)
        return qs

    def dispatch(self, request, *args, **kwargs):
        resp = super().dispatch(request, *args, **kwargs)
        user_cookie = request.COOKIES.get('user_cookie')
        if not user_cookie:
            # Visiting for the first time
            if not request.session.session_key:
                request.session.save()
            session_id = request.session.session_key
            monthly = datetime.datetime.now() + datetime.timedelta(days=30)
            monthly = datetime.datetime.replace(monthly, hour=0, minute=0, second=0)
            expires = datetime.datetime.strftime(monthly, "%a, %d-%b-%Y %H:%M:%S GMT")
            resp.set_cookie('user_cookie', session_id, expires=expires)
        if request.method == 'POST':
            thread = Thread(target=process_query, args=(resp.data['dna_sequence'], user_cookie,))
            thread.start()
        return resp


class BlastResultViewSet(viewsets.ModelViewSet):
    queryset = BlastResult.objects.all()
    serializer_class = BlastResultSerializer

    def get_queryset(self):
        user_cookie = self.request.query_params.get("user_cookie", None)
        qs = BlastResult.objects.all()
        if user_cookie:
            qs = qs.filter(user_cookie=user_cookie)
        return qs


def home(request):
    return HttpResponse('<p>Please specify an existing route.</p>')
