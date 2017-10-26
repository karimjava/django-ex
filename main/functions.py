# -*- coding: UTF-8 -*-

from . import settings
import BeautifulSoup
import urllib
import os
from django.db import transaction
from django.utils import timezone
import re

def replace_common_arabic_words(text):
    out = unicode(text)
    # print out
    for w in settings.RE_WORDS:
        out = out.replace(unicode(w[0]), unicode(w[1]))
    # print out
    return out


def fix_db():
    from ask.models import questions
    print 'start1'
    i =63642
    while i< 153235:
        if i+1000 > 153235:
            end = 153235
        else:
            end = i+1000
        qs = questions.objects.all()[i:end]
        i = i+1000
        print 'i= '+str(i)
        for q in qs:
            print str(q.id)
            q.q_text = replace_common_arabic_words(q.q_text)
            q.a_text = replace_common_arabic_words(q.a_text)
            q.save()
    return True


@transaction.atomic
def getData(url, user):
    # print user
    print user
    from ask.models import questions
    from main import functions
    data = urllib.urlopen(url)
    bs = BeautifulSoup.BeautifulSoup(data)
    if bs.contents:
        create_list = []

        next_result = bs.findAll('', attrs={'data-action': 'ItemsNext'})

        if len(next_result):
            next_result = next_result[0].attrMap
            next_result = 'https://ask.fm/' +next_result['href']
        else:
            next_result = False

        main_content = bs.findAll('', attrs={'class': re.compile(r'item streamItem streamItem-answer')})
        if len(main_content):
            for key, qans in enumerate(main_content):

                times_href = qans.findAll('', attrs={'title': True})
                time_href = times_href[0].attrMap
                t = timezone.datetime.strptime(time_href['title'], "%B %d, %Y %H:%M:%S %Z")
                print t
                if(questions.objects.filter(q_time=t).filter(owner_id=user.id).exists()):
                    print "exists"
                    questions.objects.bulk_create(create_list)
                    create_list = []
                    return False

                answers = sum([a.contents for a in qans.findAll('', attrs={'class': re.compile(r'streamItem_content')})], [])

                visualLinks = sum([a.contents for a in qans.findAll('', attrs={'class': re.compile(r'streamItemContent streamItemContent-visual')})], [])
                answers += visualLinks;

                answers = '<div class="streamItem_content">'.join([unicode(b)+"</div>" for b in answers if b!='\n'])

                quests = sum([a.contents for a in qans.findAll('', attrs={'class': re.compile(r'streamItem_header')})], [])

                quests = ' '.join([unicode(b) for b in quests if b!='\n'])
                q_text = ' '.join([a.text for a in qans.findAll('', attrs={'class': re.compile(r'streamItem_header')})])
                q_text = functions.replace_common_arabic_words(q_text)

                a_text = ' '.join([a.text for a in qans.findAll('', attrs={'class': re.compile(r'streamItem_content')})])
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
                create_list.append(question)

            questions.objects.bulk_create(create_list)
        else:
            questions.objects.bulk_create(create_list)
            return False
            # quests.remove('\n')
        if not next_result:
            questions.objects.bulk_create(create_list)

        return next_result
    else:
        questions.objects.bulk_create(create_list)
        create_list = []
        return False


def getAllData(url, user, create_list):
    # print user
    from ask.models import questions
    from main import functions
    data = urllib.urlopen(url)
    bs = BeautifulSoup.BeautifulSoup(data)
    if bs.contents:

        next_result = bs.findAll('', attrs={'data-action': re.compile(r'ItemsNext')})
        if len(next_result):
            next_result = next_result[0].attrMap
            next_result = 'https://ask.fm/' +next_result['href']
        else:
            next_result = False

        main_content = bs.findAll('', attrs={'class': re.compile(r'item streamItem streamItem-answer')})
        for key, qans in enumerate(main_content):

            times_href = qans.findAll('', attrs={'title': True})
            time_href = times_href[0].attrMap
            t = timezone.datetime.strptime(time_href['title'], "%B %d, %Y %H:%M:%S %Z")
            print t

            # if(questions.objects.filter(q_time=t).exists()):
            #     return False

            answers = sum([a.contents for a in qans.findAll('', attrs={'class': re.compile(r'streamItem_content')})], [])

            visualLinks = sum([a.contents for a in qans.findAll('', attrs={'class': re.compile(r'streamItemContent streamItemContent-visual')})], [])
            answers += visualLinks;

            answers = '<div class="streamItem_content">'.join([unicode(b)+"</div>" for b in answers if b!='\n'])

            quests = sum([a.contents for a in qans.findAll('', attrs={'class': re.compile(r'streamItem_header')})], [])

            quests = ' '.join([unicode(b) for b in quests if b!='\n'])
            q_text = ' '.join([a.text for a in qans.findAll('', attrs={'class': re.compile(r'streamItem_header')})])
            q_text = functions.replace_common_arabic_words(q_text)

            a_text = ' '.join([a.text for a in qans.findAll('', attrs={'class': re.compile(r'streamItem_content')})])
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
            create_list.append(question)
        # questions.objects.bulk_create(create_list)
            # quests.remove('\n')
        if not next_result:
            questions.objects.bulk_create(create_list)
        return next_result
    else:
        questions.objects.bulk_create(create_list)
        return False


def get_all_data():
    print 'hi'
    from ask.models import Users
    users = Users.objects.all()
    for user in users:
        fetch = True
        i = 0
        fetch = 'https://ask.fm/'+user.ask_id#+'/answers/more?page='+str(i)
        while(fetch):
            print i
            print user.ask_id

            fetch = getData(fetch, user)
            i += 1

def get_user_data(user):
        fetch = True
        i = 0
        fetch = 'https://ask.fm/'+user.ask_id#+'/answers/more?page='+str(i)
        while(fetch):
            print i
            print user.ask_id
            fetch = getData(fetch, user)
            i += 1
