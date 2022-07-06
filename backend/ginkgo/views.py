import asyncio
import json
from threading import Thread

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
import logging

from ginkgo.serializers import BlastQuerySerializer, BlastResultSerializer
from ginkgo.models import BlastQuery, BlastResult
from ginkgo.utils import lambda_logic


# Create your views here.
class BlastQueryViewSet(viewsets.ModelViewSet):
    queryset = BlastQuery.objects.all()
    serializer_class = BlastQuerySerializer

    def dispatch(self, request, *args, **kwargs):
        resp = super().dispatch(request, *args, **kwargs)
        thread = Thread(target=lambda_logic, args=(resp.data['dna_sequence'],))
        thread.start()
        # print(json.loads(request.body)['dna_sequence'])
        return resp


class BlastResultViewSet(viewsets.ModelViewSet):
    queryset = BlastResult.objects.all()
    serializer_class = BlastResultSerializer


def home(request):
    return HttpResponse('<p>Please specify an existing route.</p>')
