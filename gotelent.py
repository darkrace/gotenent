
import requests
import re, json
from lxml import etree
from bs4 import BeautifulSoup as bsp
from io import StringIO
import smtplib, ssl
fl = open("data.txt",'r')
fl = fl.read()
def send_maili(title, description, status):
    gmail_user = 'mailtester946@gmail.com'
    gmail_app_password = '123@abc.'
    sent_from = gmail_user
    sent_to = ['mailforapptestings2@gmail.com','nathan.pamart@gmail.com','kalathiyaalpesh@gmail.com']
    # sent_to = ['mailforapptestings2@gmail.com']
    sent_subject = title
    sent_body = (f"TITLE: {title}\n\nSTATUS:{status}\n\n DESCRIPTION:\n\t\t{description}\n\n".encode('ascii', 'ignore').decode('ascii'))

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(sent_to), sent_subject, sent_body)


    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context(), timeout=20) as server:
            # server.connect(host='smtp.gmail.com', port=465)

            server.ehlo()
            server.login(user=gmail_user, password=gmail_app_password)
            server.sendmail(sent_from, sent_to, email_text)
            server.close()

        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)

sess = requests.session()
req = sess.get("https://app.gocatalant.com/c/_/auth/login/")
soup = bsp(req.text, 'lxml')
form = soup.find(lambda tag: tag.name == 'form' and tag.get('id', '') == 'login-form')

inputs = form.find_all('input')
form_data = {}
for i in inputs:
    try:
        form_data[i['name']] = i['value']
    except:
        pass
form_data['email'] = "nathan.pamart@gmail.com"
form_data['password'] ="qeQku5-weqgeb-jevvyv"

req1 = sess.post("https://app.gocatalant.com/c/_/auth/login/", json=form_data)
req2 = sess.get("https://app.gocatalant.com/c/_/u/0/search/",cookies=req1.cookies)
pg=1
fst = ""
flag = True
while flag:
    page_src = StringIO(req2.text)
    htpars = etree.HTMLParser()
    tree = etree.parse(page_src, htpars)
    for x in range(1,10):
        title = "".join(tree.xpath("(//div[@class='need-card-inline'])["+str(x)+"]//div[@class='row need-card-inline-name']//span/text()"))
        description = " ".join(tree.xpath("(//div[@class='need-card-inline'])["+str(x)+"]//div[contains(@class,'need-card-inline-details')]//p[contains(@class,'text-muted')]/text()"))
        status = "".join(tree.xpath("((//div[@class='search-result'])["+str(x)+"]//div[@class='need-card-inline']/div[@class='small']/text())[last()]"))
        data=",".join([title,description,status])
        if fst == "":
            with open("data.txt", "w+") as f:
                f.write(data)
            fst = data
        if data != fl:
            print("a")
            send_maili(title,description,status)
        else:
            print("e")

            flag = False
            pg+=1
            break
    print("L")
    req2 = sess.get(f"https://app.gocatalant.com/c/_/u/0/search/?need_page={pg}", cookies=req1.cookies)


print(req)



