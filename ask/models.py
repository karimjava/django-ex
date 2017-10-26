# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
from django.utils.timesince import timesince
from django.template.defaultfilters import date as _date
# Create your models here.
# from main import functions
from django.db import transaction

class Result(models.Model):
    """Users Pages Model."""
    number_id = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)


class Users(models.Model):
    """Users Pages Model."""
    name = models.CharField(max_length=128)
    ask_id = models.CharField(max_length=128)
    image_path = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            with transaction.atomic():
                super(Users, self).save(*args, **kwargs)
                fetch = True
                i = 0
                fetch = 'https://ask.fm/'+self.ask_id#+'/answers/more?page='+str(i)
                created_list = []
                from main import functions
                while(fetch):
                    print i
                    fetch = functions.getAllData(fetch, self, created_list)
                    i+=1

                # import gevent
                # import gevent.monkey
                # gevent.monkey.patch_all()
                # INTERVAL = 24*60*60
                # def callback():
                #     from main import functions
                #     functions.get_user_data(self)
                # def loop():
                #     while True:
                #         callback()
                #         gevent.sleep(INTERVAL)

                # gevent.Greenlet.spawn(loop)

        else:
            super(Users, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class questions(models.Model):
    """Questions Model."""
    question_html = models.TextField()
    answer_html = models.TextField()
    q_time = models.DateTimeField()
    href = models.CharField(max_length=128)
    q_text = models.TextField()
    a_text = models.TextField()
    owner = models.ForeignKey(Users, related_name="questions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def q_html(self):
        regex = re.compile(r'<a \S+questionersName(.*)<\/a>')
        out = re.sub(regex, '', self.question_html)
        # print out
        return out

    @property
    def q_stime(self):
        return '%(time)s' % {'time':_date(self.q_time, 'l , d E Y | h:i A')}
        # print out


    def __unicode__(self):
        return self.q_text
