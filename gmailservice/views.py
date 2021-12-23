from django.shortcuts import render
from .forms import loginForm
import smtplib
import imaplib
import email
from email.parser import BytesParser
from email import policy
# Create your views here.
def index(request):
    
    context={'login':loginForm}
    return render(request,'gmailservice/login.html',context)

def login(request):
    id = request.GET['id']
    pas = request.GET['pas']
    gmail = imaplib.IMAP4_SSL("imap.gmail.com", '993')
    gmail.login(id, pas)
    gmail.select()

    # ALLでSearchすると指定したラベルの全てのメールを読み込む
    
    head, data = gmail.search(None, 'ALL')
    datas = data[0].split()
    fetch_num = 20
    if (len(datas)-fetch_num)<0:
        fetch_num = len(datas)
    msg_list = []
    for num in datas[len(datas)-fetch_num::]:
        typ , data = gmail.fetch(num,'(RFC822)')
        raw_email=data[0][1]
        m = BytesParser(policy=policy.default).parsebytes(data[0][1])
        from_ = m.get('From',failobj='')
        msg = email.message_from_string(raw_email.decode('utf-8'))
        msg_encoding = email.header.decode_header(msg.get('Subject'))[0][1] or 'iso-2020-jp'
        msg_subject = email.header.decode_header(msg.get('Subject'))[0][0]
        subject = str(msg_subject.decode(msg_encoding))
        body = msg.get_payload()
        msg_list.append([from_,subject]) 
    gmail.close()
    gmail.logout() 
    context={'head':head,'data':data,'list':msg_list}
    return render(request,'gmailservice/list.html',context)
def list(request):
    return render(request,'gmailservice/list.html')

def count(request):
    return render(request,'gmailservice/count.html')