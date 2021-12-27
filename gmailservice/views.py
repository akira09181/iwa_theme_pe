from django.shortcuts import render
from .forms import loginForm
import smtplib
import imaplib
import email
from email.parser import BytesParser
from email import policy
from .models import Mails
import datetime
# Create your views here.
def index(request):
    
    context={'login':loginForm}
    return render(request,'gmailservice/login.html',context)

def login(request):
    id = request.GET['id']
    pas = request.GET['password']
    gmail = imaplib.IMAP4_SSL("imap.gmail.com", '993')
    gmail.login(id, pas)
    gmail.select()
    dt = datetime.datetime.today()
    today = str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)
   
    
    head, data = gmail.search(None, 'ALL')
    datas = data[0].split()
    fetch_num = 500
    if (len(datas)-fetch_num)<0:
        fetch_num = len(datas)
    msg_list = []
    for num in datas[len(datas)-fetch_num::]:
        typ , data = gmail.fetch(num,'(RFC822)')
        raw_email=data[0][1]
        m = BytesParser(policy=policy.default).parsebytes(data[0][1])
        from_ = m.get('From',failobj='')
        dat = m.get('Date')
        
        msg = email.message_from_string(raw_email.decode('utf-8'))
        msg_encoding = email.header.decode_header(msg.get('Subject'))[0][1] or 'iso-2020-jp'
        msg_subject = email.header.decode_header(msg.get('Subject'))[0][0]
        subject = str(msg_subject.decode(msg_encoding))
        body = msg.get_payload()
        msg_list.append([from_,subject]) 
        a = Mails(name=id,date=dt,domain=from_,title=subject)
        b = Mails.objects.filter(title=subject).count()
        if b == 1:
            break
        a.save()
    
    gmail.close()
    gmail.logout() 
    context={'head':head,'data':data,'list':msg_list}
    return render(request,'gmailservice/list.html',context)
def list(request):
    
    
    return render(request,'gmailservice/list.html')

def count(request):
    b = Mails.objects.all().values()
    result = [[0,'']for i in range(len(b))]
    for i in range(len(b)):
        result[i][1]=b[i]['domain']
        result[i][0]+=1
    context={'value':result}
    return render(request,'gmailservice/count.html',context)