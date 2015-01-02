from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
import json
import re
import random
import hashlib


from expense.models import *

from django.core import serializers
import logging
logger = logging.getLogger(__name__)


class foo:
    def __init__(self,ques_id):
        self.counter=-1
        self.ques_id=ques_id
    def __call__(self,mob):
        self.counter+=1
        return '<a href="#"'\
                'class="code" '\
                'id="blank'+str(self.counter)+'" '\
                'data-type="select2" '\
                'data-pk="'+ hashlib.md5(mob.string).hexdigest()+'" '\
                'data-url="/question/'+str(self.ques_id)+'/'+str(self.counter)+'/" '\
                'data-source="/answers/'+str(self.ques_id)+'/'+str(self.counter)+'/" '\
                '>_______</a>'

qdata=[
        {
            'q':'fiil in the banks for the value to be true',
            'c':'i ::blank:: 2  ',
            'a':[['==','<','>','!='],['4','2','3','1']]
        },
        {
            'q':'complete the function defination',
            'c':'::blank:: foo(bar1,bar2)::blank:: \n'\
                '           ::blank:: \"Hello World\" ',
            'a':[['def','while','for','if'],[':',';','-','*'],['print','dump','put','None']]
        },
        {
            'q': 'what should be the condition so that value of i is printed only when i is even?',
            'c': 'def foo(i): \n'\
                    '    if ((::blank:: ::blank:: 2) ==0) is ::blank::: \n'\
                    '        ::blank:: i',
            'a': [['i','j','k','l'],['%','*','+','-'],['True','False','while','1'],['print','put','str','import']],
        },
        {
            'q': 'Complete the list comprehension to print the sum of square first 10 natural numbers',
            'c': 'print sum([::blank:: ::blank:: ::blank:: for i in ::blank::(10)])',
            'a': [['i','j','k','l'],['*','%','+','-'],['i','a','b','c'],['range','all','numbers','natural_number']],
        },
     ]


for q in qdata:
    q['id']=hashlib.md5(q['c']).hexdigest()


def question(request,ques_id,ans_id=None):
    resdict = {}
    ques_id = int(ques_id)
    if request.method == 'POST':
        ques=[q for q in qdata if q['id']==request.POST['pk']][0]#int(request.POST['pk'])
        if ans_id is None:
            return HttpResponseBadRequest('Wrong Answere',content_type='text/plain')
        ans_id=int(ans_id)
        if request.POST['value'] in ques['a'][ans_id] and ques['a'][ans_id].index(request.POST['value']) == 0:
            return HttpResponse('OK',content_type='text/plain')
        else:
            return HttpResponseBadRequest('Wrong Answere',content_type='text/plain')
    elif request.method == 'GET':
        resdict['pk']=ques_id
        resdict['c']=re.subn('::blank::',foo(ques_id),qdata[ques_id]['c'])[0]
        resdict['q']=qdata[ques_id]['q']
        return render(request, 'q.html',resdict)
    return HttpResponseNotFound()


def answers(request, ques_id, ans_id):
    try:
        l=[{'id':str(ans),'text':str(ans)}  for ans in qdata[int(ques_id)]['a'][int(ans_id)]]
        random.shuffle(l)
        return HttpResponse(json.dumps(l),content_type='text/javascript')
    except Exception,e: 
        return HttpResponseBadRequest((str(e)))



