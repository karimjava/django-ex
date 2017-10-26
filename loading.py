# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import BeautifulSoup
import urllib
# import pandas as pd
# import numpy as np
# from . import models
# from .models import questions
import os
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def getData(url, user):
    # print user
    from ask.models import questions
    data = urllib.urlopen(url)
    bs = BeautifulSoup.BeautifulSoup(data)
    if bs.contents:
        next_result = bs.findAll('', attrs={'class': 'viewMore'})
        if len(next_result):
            next_result = next_result[0].attrMap
            next_result = 'https://ask.fm/' +next_result['data-url']
        else:
            next_result = False
        data_questions = bs.findAll('', attrs={'class': 'streamItemContent streamItemContent-question'})
        answers = bs.findAll('', attrs={'class': 'streamItemContent streamItemContent-answer'})
        times_href = bs.findAll('', attrs={'data-hint': True})
        # times_href = times_href.attrMap

        for key, d in enumerate(data_questions):
            time_href = times_href[key].attrMap
            t = timezone.datetime.strptime(time_href['data-hint'], "%B %d, %Y %H:%M:%S %Z")
            if(questions.objects.filter(q_time=t).exists()):
                print key
                return next_result
            question = questions()
            print(d, answers[key])
            q = [unicode(x) for x in (d.findAll("span")[0]).contents]
            ans = [unicode(x) for x in (answers[key].findAll("span")[0]).contents]
            question.href = unicode(time_href['href'])
            q = ' '.join(q)
            question.question = q
            # print ans
            question.answer = ' '.join(ans)
            question.owner_id = user.id
            question.q_time = t

            question.save()
        return next_result
    else:
        return False


@transaction.atomic
def getAllData(url, user):
    # print user
    from ask.models import questions
    from main import functions
    data = urllib.urlopen(url)
    bs = BeautifulSoup.BeautifulSoup(data)
    if bs.contents:
        next_result = bs.findAll('', attrs={'class': 'ItemsNext'})
        if len(next_result):
            next_result = next_result[0].attrMap
            next_result = 'https://ask.fm/' +next_result['href']
        else:
            next_result = False

        main_content = bs.findAll('', attrs={'class': 'item streamItem streamItem-answer'})
        for key, qans in enumerate(main_content):
            times_href = qans.findAll('', attrs={'title': True})
            time_href = times_href[0].attrMap
            t = timezone.datetime.strptime(time_href['title'], "%B %d, %Y %H:%M:%S %Z")
            # if(questions.objects.filter(q_time=t).exists()):
            #     return False

            answers = sum([a.contents for a in qans.findAll('', attrs={'class': 'streamItem_content'})], [])

            visualLinks = sum([a.contents for a in qans.findAll('', attrs={'class': 'streamItemContent streamItemContent-visual'})], [])
            answers += visualLinks;

            answers = ' '.join([unicode(b) for b in answers if b!='\n'])

            quests = sum([a.contents for a in qans.findAll('', attrs={'class': 'streamItem_header'})], [])

            quests = ' '.join([unicode(b) for b in quests if b!='\n'])
            q_text = ' '.join([a.text for a in qans.findAll('', attrs={'class': 'streamItem_header'})])
            q_text = functions.replace_common_arabic_words(q_text)

            a_text = ' '.join([a.text for a in qans.findAll('', attrs={'class': 'streamItem_content'})])
            a_text = functions.replace_common_arabic_words(a_text)



            question = questions()
            question.question_html = quests
            # print ans
            question.href = unicode(time_href['href'])
            question.answer_html = answers
            question.q_text = q_text
            question.a_text = a_text

            question.q_time = t
            question.owner_id = user.id
            question.save()
            # quests.remove('\n')
        return next_result
    else:
        return False


if __name__ == '__main__':
    from django.core.wsgi import get_wsgi_application
    # from ask_app import settings
    # from django.core.management import setup_environ
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_app.settings")
    application = get_wsgi_application()
    from main import functions
    functions.get_all_data()


    # print user
