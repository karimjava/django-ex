# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import filters
from django.db.models import Q
from . import functions

class MainOrdereringFilter(filters.BaseFilterBackend):
    """
    Filter with ordering from frontend default orderBy q_time desc.
    """

    def filter_queryset(self, request, queryset, view):

        order_by = request.query_params.get('order_by', '-q_time')
        try:
            queryset.order_by(order_by).exists()
            return queryset.order_by(order_by)
        except:
            return queryset


class MainSearchFilter(filters.BaseFilterBackend):
    """
    Filter with filter by and contain q.
    """

    def filter_queryset(self, request, queryset, view):
        filter_by = request.query_params.get('filter_by', None)
        q = request.query_params.get('q', None)

        if filter_by and q:
            try:
                q = functions.replace_common_arabic_words(q)
                return queryset.filter(Q(q_text__contains= q) | Q(a_text__contains= q))
            except:
                return queryset
        elif q:
            # fields = libs.get_fields(view.model)
            q_objs = [Q(**{'%s__contains' % i: q}) for i in fields]
            queries = reduce(lambda x, y: x | y, q_objs)
            return queryset.filter(queries)

        else:
            return queryset


class OwnerSearchFilter(filters.BaseFilterBackend):
    """
    Filter with filter by and contain q.
    """

    def filter_queryset(self, request, queryset, view):
        user_id = request.query_params.getlist('user_id', None)
        #print (user_id, 'hi')
        if user_id:
            return queryset.filter(owner_id__in= user_id)

        else:
            return queryset
