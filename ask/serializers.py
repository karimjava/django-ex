# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    """Users Serializer."""

    class Meta:
        model = Users
        fields = ('id', 'name', 'image_path','ask_id')
        read_only_fields = ('created_at', 'updated_at')

class ResultSerializers(serializers.ModelSerializer):
    """Result Serializer."""

    class Meta:
        model = Result
        fields = ('number_id', 'phone_number')
        read_only_fields = ('created_at', 'updated_at')


class QuestionSerializers(serializers.ModelSerializer):
    """State Serializer."""

    class Meta:
        model = questions
        depth=1
        fields = ('id','url', 'q_html', 'answer_html', 'q_time', 'owner', 'href','q_stime','q_text')
        read_only_fields = ('created_at', 'updated_at')
