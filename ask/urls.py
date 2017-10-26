# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import include, url
from rest_framework import routers
# from django.contrib import admin
from .views import *
from . import tasks

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'questions', QuestionsViewSet)
router.register(r'results', ResultViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


urlpatterns = [
    url(r'^', include(router.urls)),
]
