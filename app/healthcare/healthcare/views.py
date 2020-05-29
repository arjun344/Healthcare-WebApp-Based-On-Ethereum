import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests
from django.middleware.csrf import get_token
import json
from web3 import Web3
from hexbytes import HexBytes
from hashlib import sha256
import datetime
import base64

class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


url = "http://127.0.0.1:8543"
web3 = Web3(Web3.HTTPProvider(url))
web3.eth.defaultAccount = web3.eth.accounts[0]
address = web3.toChecksumAddress("0xa9Dda1C8cCda9b6aec35f49B2C1C49607D6f1dce")

with open('abi/abi.json') as f:
  abi = json.load(f)

unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",15000)
contract = web3.eth.contract(address=address,abi=abi)


patient_logged_id = None
doctor_logged_id = None


def index(request):
	csrf_token = get_token(request)
	return render(request,'index.html')

def AddPatient(request):

	if request.is_ajax():
		request_data = request.POST
		name = request_data['name']
		emailid = request_data['emailid']
		uniqueid = request_data['uniqueid']
		password = request_data['password']

		unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",1500)

		if unlocked:
			temp = contract.functions.setUserProfile(name,emailid,uniqueid,password).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)
		
	return render(request,'index.html')

def AddDoctor(request):

	if request.is_ajax():
		request_data = request.POST
		name = request_data['name']
		emailid = request_data['emailid']
		uniqueid = request_data['uniqueid']
		licenseid = request_data['licenseid']
		organization = request_data['organization']
		password = request_data['password']

		unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",1500)

		if unlocked:
			temp = contract.functions.setDoctorProfile(name,emailid,uniqueid,licenseid,organization,password).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)
		
	return render(request,'index.html')

def AddInsurer(request):

	if request.is_ajax():
		request_data = request.POST
		name = request_data['name']
		emailid = request_data['emailid']
		licenseid = request_data['licenseid']
		password = request_data['password']

		unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",1500)

		if unlocked:
			temp = contract.functions.setInsurerProfile(name,emailid,licenseid,password).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)
		
	return render(request,'index.html')


def LoginUser(request):
	global patient_logged_id
	if request.is_ajax():
		request_data = request.POST
		emailid = request_data['emailid']
		password = request_data['password']

		count = contract.functions.getUserCounter().call()

		for user in range(count):
			email = contract.functions.UserLoginInfo(user).call()[0]
			pas = contract.functions.UserLoginInfo(user).call()[1]

			if email == emailid and pas == password:
				dic = {'id':user,'emailid':email}
				patient_logged_id = user
				data = json.dumps(dic)
				return JsonResponse(data, safe=False)

		dic = [-1]
		data = json.dumps(dic)
		return JsonResponse(data, safe=False)
		
	return render(request,'index.html')

def LoginDoctor(request):

	if request.is_ajax():
		request_data = request.POST
		emailid = request_data['emailid']
		password = request_data['password']

		count = contract.functions.getDoctorCounter().call()

		for user in range(count):
			email = contract.functions.DoctorLoginInfo(user).call()[0]
			pas = contract.functions.DoctorLoginInfo(user).call()[1]

			if email == emailid and pas == password:
				dic = {'id':user,'emailid':email}
				data = json.dumps(dic)
				return JsonResponse(data, safe=False)

		dic = [-1]
		data = json.dumps(dic)
		return JsonResponse(data, safe=False)
		
	return render(request,'index.html')

def LoginInsurer(request):

	if request.is_ajax():
		request_data = request.POST
		emailid = request_data['emailid']
		password = request_data['password']

		count = contract.functions.getInsurerCounter().call()

		for user in range(count):
			email = contract.functions.InsurerLoginInfo(user).call()[0]
			pas = contract.functions.InsurerLoginInfo(user).call()[1]

			if email == emailid and pas == password:
				dic = {'id':user,'emailid':email}
				data = json.dumps(dic)
				return JsonResponse(data, safe=False)

		dic = [-1]
		data = json.dumps(dic)
		return JsonResponse(data, safe=False)
		
	return render(request,'index.html')


def patient(request):
	csrf_token = get_token(request)
	if patient_logged_id is None:
		return render(request,'index.html')

	patient_data = contract.functions.UserInfo(patient_logged_id).call()
	doc_size = patient_data[3]
	ins_size = patient_data[4]
	patient_doc_data = []
	patient_insurer_data = []
	rep_size = patient_data[5]
	med_report = []
	med_img_report_name = []
	doctor_list = []

	for i in range(ins_size):
		insurer = contract.functions.InsOfUser(patient_logged_id,i).call()
		patient_insurer_data.append(insurer)


	count = contract.functions.getDoctorCounter().call()
	for doc in range(count):
		temp = contract.functions.DoctorInfo(doc).call()
		doctor_list.append(temp)

	for item in range(rep_size):
	    temp = contract.functions.MedOfUser(patient_logged_id,item).call()
	    med_report.append(temp)

	for item in range(doc_size):
		temp = contract.functions.DoccOfUser(patient_logged_id,item).call()
		patient_doc_data.append(temp)

	for item in range(rep_size):
		temp = contract.functions.MedOfUser(patient_logged_id,item).call()
		temp2 = temp[2].split(",")
		temp2 = temp2[:-1]
		med_img_report_name.append(temp2)

	insurer_size = contract.functions.getInsurerCounter().call()
	insurer_list = []

	for item in range(insurer_size):
		temp = contract.functions.InsurerInfo(item).call()
		insurer_list.append(temp)

	base_img_data = []
	for rep in med_img_report_name:
		temp = []
		for fname in rep:
			data = open(fname, "r").read()
			data = data[2:-1]
			temp.append(data)
		base_img_data.append(temp)

	return render(request,'patient.html',{'base_img_data':base_img_data,'doctor_list':doctor_list,'med_report':med_report,'patient_logged_id':patient_logged_id,'insurer_list':insurer_list,'patient_data':patient_data,'patient_doc_data':patient_doc_data,'patient_insurer_data':patient_insurer_data})

def doctor(request):
	csrf_token = get_token(request)
	global doctor_logged_id
	doctor_logged_id = 0

	doctor_data = contract.functions.DoctorInfo(doctor_logged_id).call()

	patient_size = contract.functions.DoctorLoginInfo(doctor_logged_id).call()[2]

	doc_patient_data = []

	for i in range(patient_size):
		patient_data = contract.functions.PatOfDoc(doctor_logged_id,i).call()
		data,pat_id = getPatId(patient_data[2])
		temp = [pat_id]
		data = data + temp
		med_report = getMedReport(pat_id)
		data = data + med_report
		doc_patient_data.append(data)

	non_verified = []

	for patient in doc_patient_data:
		for report in range(len(patient[7])):
			if str(patient[7][report][4]) == "0" and str(patient[7][report][3]) == str(doctor_data[3]):
				temp = []
				temp.append(patient[7][report])
				temp.append([patient[8][report]])
				temp.append(patient[1])
				temp.append(patient[6])

				non_verified.append(temp)

	return render(request,'doctor.html',{'non_verified':non_verified,'doctor_logged_id':doctor_logged_id,'doctor_data':doctor_data,'doc_patient_data':doc_patient_data})

def getMedReport(pat_id):
	med_report = []
	med_img_report_name = []

	rep_size = contract.functions.UserInfo(pat_id).call()[5]

	for item in range(rep_size):
		temp = contract.functions.MedOfUser(pat_id,item).call()
		med_report.append(temp)

	for item in range(rep_size):
		temp = contract.functions.MedOfUser(pat_id,item).call()
		temp2 = temp[2].split(",")
		temp2 = temp2[:-1]
		med_img_report_name.append(temp2)

	base_img_data = []

	for rep in med_img_report_name:
		temp = []
		for fname in rep:
			data = open(fname, "r").read()
			data = data[2:-1]
			temp.append(data)
		base_img_data.append(temp)

	combined = [med_report,base_img_data]
	return combined


def getPatId(uniqueid):
	user_counter = contract.functions.getUserCounter().call()
	for i in range(user_counter):
		user_data = contract.functions.UserInfo(i).call()
		if uniqueid in user_data:
			return user_data,i
	return None,None

def AddinsToUsr(request):
	csrf_token = get_token(request)
	if request.is_ajax():
		request_data = request.POST
		insid = int(request_data['insid'])
		patid = int(request_data['patid'])

		unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",1500)

		if unlocked:
			temp = contract.functions.AddInsToUsr(patid,insid).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)

	return render(request,'index.html')

def AdddocToUsr(request):
	csrf_token = get_token(request)
	if request.is_ajax():
		request_data = request.POST
		docid = int(request_data['docid'])
		patid = int(request_data['patid'])

		unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",1500)

		if unlocked:
			temp = contract.functions.AddDocToPat(patid,docid).transact()
			temp2 = contract.functions.AddPatToDoc(docid,patid).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			while web3.eth.getTransaction(temp2)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)

	return render(request,'index.html')

def AddMedicalRecord(request):
	csrf_token = get_token(request)
	if request.is_ajax():
		request_data = request.POST
		disease = request_data['disease']
		report = request_data['report']

		imglst = report.split("***")
		imglst = imglst[:-1]
		
		fileNamelst = ""

		for img in imglst:
			img = str(img).encode('utf-8')
			hashedWord = sha256(img.strip()).hexdigest()
			imgname = "MedicalRecords/"+str(hashedWord) + str(datetime.datetime.now().timestamp())
			print(imgname)
			fileNamelst =fileNamelst+imgname+","
			with open(imgname, "w") as text_file:
				text_file.write(str(img))

		license = request_data['license']
		unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",1500)

		if unlocked:
			temp = contract.functions.AddMedicalRecord(patient_logged_id,disease,fileNamelst,license).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)

	return render(request,'index.html')

def UpdateMedicalRecord(request):
	csrf_token = get_token(request)
	if request.is_ajax():
		request_data = request.POST
		rep_id = request_data['repid']
		disease = request_data['disease']
		report = request_data['report']

		imglst = report.split("***")
		imglst = imglst[:-1]
		
		fileNamelst = ""

		for img in imglst:
			img = str(img).encode('utf-8')
			hashedWord = sha256(img.strip()).hexdigest()
			imgname = "MedicalRecords/"+str(hashedWord) + str(datetime.datetime.now().timestamp())
			print(imgname)
			fileNamelst =fileNamelst+imgname+","
			with open(imgname, "w") as text_file:
				text_file.write(str(img))

		license = request_data['license']
		unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",1500)

		if unlocked:
			temp = contract.functions.UpdateReport(int(patient_logged_id),int(rep_id),disease,fileNamelst,license).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)

	return render(request,'index.html')


def UpdateRepStats(request):
	csrf_token = get_token(request)
	if request.is_ajax():
		request_data = request.POST
		rep_id = request_data['rep_id']
		pat_id = request_data['pat_id']
		unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",1500)

		if unlocked:
			temp = contract.functions.UpdateReportStats(int(pat_id),int(rep_id),"1").transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)

	return render(request,'doctor.html')




def DeleteMedicalRecord(request):
	csrf_token = get_token(request)
	if request.is_ajax():
		request_data = request.POST
		rep_id = request_data['repid']
		unlocked = web3.geth.personal.unlockAccount(web3.geth.personal.listAccounts()[0],"1",1500)

		if unlocked:
			temp = contract.functions.DeleteRecord(int(patient_logged_id),int(rep_id)).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)

	return render(request,'index.html')

