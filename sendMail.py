import smtplib
import json
from email.mime.text import MIMEText
from email.utils import formataddr

my_name='YourName'
my_mail='YourEmail'
my_pw="YourPassWord"
source='localization.json'
templateDem='templateDem.txt'
templateGop='templateGop.txt'

def sendMail(target,content,receiver):
	try:
		msg=MIMEText(content,'plain','utf-8')
		msg['From']=formataddr([my_name,my_mail])
		msg['To']=formataddr([receiver,target])
		msg['Subject']='My concern regarding S.386'

		server=smtplib.SMTP('smtp.office365.com',587)#This depends on the Email you are using
		server.starttls()
		'''
		If you are using gmail:
		server = smtplib.SMTP(smtp.gmail.com, 587)
		Also you need to enable SMTP service of your Email first
		'''
		server.login(my_mail,my_pw)
		server.sendmail(my_mail,[target,],msg.as_string())

		server.quit()
		print("Mail delivered to: "+target)
		return True
	except e:
		print(str(e))
		print("Failed to deliver: "+target)
		return False
		


def parseJson():
	dems=[]
	gops=[]
	inputFile=open(source)
	obj=json.load(inputFile)
	for rep in obj['Schedulers 2019']:
		if 'Last' in rep and rep['Legislator Title']=='Senator':
			repItem={'name':rep['Last'],'mail':rep['Email']}
			if rep['Party']=='R':
				gops.append(repItem)
			else:
				dems.append(repItem)
	return dems,gops


def createContent(template):
	inputFile=open(template,encoding="utf8")
	content=inputFile.read()
	content=content+'\n'+my_name
	return content


print('Start sending mails')	
dems,gops=parseJson()
for rep in dems:
	print('Sending to'+ rep['name'])
	demContent='Dear senator ' + rep['name'] + ',\n' +createContent(templateDem)
	sendMail(rep['mail'],demContent,rep['name'])
for rep in gops:
	print('Sending to'+ rep['name'])
	gopContent='Dear senator ' + rep['name'] + ',\n' +createContent(templateGop)
	sendMail(rep['mail'],gopContent,rep['name'])
print('done')	
