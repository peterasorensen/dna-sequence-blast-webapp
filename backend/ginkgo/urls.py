from django.urls import path, include
from rest_framework import routers

from ginkgo.views import BlastQueryViewSet, BlastResultViewSet

router = routers.DefaultRouter()
router.register(r'blastquery', BlastQueryViewSet)
router.register(r'blastresult', BlastResultViewSet)

urlpatterns = [
    path('', include(router.urls))
]
