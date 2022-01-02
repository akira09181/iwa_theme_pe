from django.shortcuts import render
from .forms import loginForm
import smtplib
import imaplib
import email
from email.parser import BytesParser
from email import policy
from .models import Mails
import datetime
from pprint import pprint
# Create your views here.
def index(request):
    
    context={'login':loginForm}
    return render(request,'gmailservice/login.html',context)

def login(request):
    id = request.GET['id']
    pas = request.GET['password']
    gmail = imaplib.IMAP4_SSL("imap.gmail.com", '993')
    gmail.login(id, pas)
    c = gmail.list()
    pprint(c[1])
    gmail.select('theme')
    dt = datetime.datetime.today()
    today = str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)
    d = Mails.objects.all()
    d.delete()
    
    head, data = gmail.search(None, 'ALL')
    datas = data[0].split()
    fetch_num = 500
    if (len(datas)-fetch_num)<0:
        fetch_num = len(datas)
    msg_list = []
    b = 0
    for num in datas[len(datas)-fetch_num::]:
        b+=1
        typ , data = gmail.fetch(num,'(RFC822)')
        raw_email=data[0][1]
        m = BytesParser(policy=policy.default).parsebytes(data[0][1])
        from_ = m.get('From',failobj='')
        dat = m.get('Date')
        sub = m.get('Subject')
        fr=""
        flag = 0
        for i in range(len(from_)):
            if from_[i]=='@':
                flag=1
            if from_[i]==">":
                break
            if flag==1:
                fr+=from_[i]
        #msg = email.message_from_string(raw_email.decode('utf-8'))
        #msg_encoding = email.header.decode_header(msg.get('Subject'))[0][1] or 'iso-2020-jp'
        #msg_subject = email.header.decode_header(msg.get('Subject'))[0][0]
        #subject = str(msg_subject.decode(msg_encoding))
        msg_list.append([b,dat,fr,sub]) 
        
    gmail.close()
    gmail.logout() 
    for i in range(len(msg_list)):
        
        
        a = Mails(no=msg_list[i][0],date=msg_list[i][1],domain=msg_list[i][2],title=msg_list[i][3],now=dt)
        a.save()
    context={'head':head,'data':data,'list':msg_list}
    return render(request,'gmailservice/list.html',context)
def list(request):
    b = Mails.objects.all().values()
    a = [[0,"","",""]for i in range(len(b))]
    for i in range(len(b)):
        a[i][0]=b[i]['no']
        a[i][1]=b[i]['date']
        a[i][2]=b[i]['domain']
        a[i][3]=b[i]['title']
    context={'list':a}
    return render(request,'gmailservice/list.html',context)

def count(request):
    b = Mails.objects.all().values()
    e = Mails.objects.distinct().values_list('domain')
    
    a = []
    for i in range(len(b)):
        a.append(b[i]['domain'])
    
    
    c = [[0,""]for i in range(len(e))]
    for i in range(len(e)):
            
        c[i][1]=e[i][0]
    
    
    result = [[0,'']for i in range(len(e))]
    for i in range(len(b)):
        for j in range(len(e)):
            if b[i]['domain']==c[j][1]:
                c[j][0]+=1
    c.sort(reverse=True)
    context={'value':c}
    return render(request,'gmailservice/count.html',context)