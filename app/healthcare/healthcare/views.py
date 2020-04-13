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
address = web3.toChecksumAddress("0x644315550908961c8b09b0187117C6BB1Cd1992c")
abi = json.loads('[{"constant":false,"inputs":[{"name":"_ins","type":"uint256"},{"name":"_usr","type":"uint256"}],"name":"AddUsrToIns","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_pat","type":"uint256"},{"name":"_doc","type":"uint256"}],"name":"AddDocToPat","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"InsurerLoginInfo","outputs":[{"name":"email","type":"string"},{"name":"password","type":"string"},{"name":"UsrOfInsSize","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"name":"InsOfUser","outputs":[{"name":"name","type":"string"},{"name":"email","type":"string"},{"name":"license","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"UserLoginInfo","outputs":[{"name":"email","type":"string"},{"name":"password","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_doc","type":"uint256"},{"name":"_pat","type":"uint256"}],"name":"AddPatToDoc","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"name":"PatOfDoc","outputs":[{"name":"name","type":"string"},{"name":"email","type":"string"},{"name":"uniqueid","type":"string"},{"name":"DoccOfUserSize","type":"uint256"},{"name":"InsOfUserSize","type":"uint256"},{"name":"MedicalRecordSize","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_name","type":"string"},{"name":"_email","type":"string"},{"name":"_license","type":"string"},{"name":"_password","type":"string"}],"name":"setInsurerProfile","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_usr","type":"uint256"},{"name":"_ins","type":"uint256"}],"name":"AddInsToUsr","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_userid","type":"uint256"},{"name":"_recordid","type":"uint256"},{"name":"_rep","type":"string"}],"name":"UpdateReport","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"DoctorInfo","outputs":[{"name":"name","type":"string"},{"name":"email","type":"string"},{"name":"uniqueid","type":"string"},{"name":"license","type":"string"},{"name":"organization","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getUserCounter","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_name","type":"string"},{"name":"_email","type":"string"},{"name":"_uniqueid","type":"string"},{"name":"_password","type":"string"}],"name":"setUserProfile","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"name":"MedOfUser","outputs":[{"name":"id","type":"uint256"},{"name":"disease","type":"string"},{"name":"reports","type":"string"},{"name":"doclicense","type":"string"},{"name":"verified","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_userid","type":"uint256"},{"name":"_recordid","type":"uint256"},{"name":"_stats","type":"string"}],"name":"UpdateReportStats","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"InsurerInfo","outputs":[{"name":"name","type":"string"},{"name":"email","type":"string"},{"name":"license","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getDoctorCounter","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_user","type":"uint256"},{"name":"_disease","type":"string"},{"name":"_report","type":"string"},{"name":"_doclicense","type":"string"}],"name":"AddMedicalRecord","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"UserInfo","outputs":[{"name":"name","type":"string"},{"name":"email","type":"string"},{"name":"uniqueid","type":"string"},{"name":"DoccOfUserSize","type":"uint256"},{"name":"InsOfUserSize","type":"uint256"},{"name":"MedicalRecordSize","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getInsurerCounter","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"name":"DoccOfUser","outputs":[{"name":"name","type":"string"},{"name":"email","type":"string"},{"name":"uniqueid","type":"string"},{"name":"license","type":"string"},{"name":"organization","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"name":"UsrOfIns","outputs":[{"name":"name","type":"string"},{"name":"email","type":"string"},{"name":"uniqueid","type":"string"},{"name":"DoccOfUserSize","type":"uint256"},{"name":"InsOfUserSize","type":"uint256"},{"name":"MedicalRecordSize","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_name","type":"string"},{"name":"_email","type":"string"},{"name":"_uniqueid","type":"string"},{"name":"_license","type":"string"},{"name":"_organisation","type":"string"},{"name":"_password","type":"string"}],"name":"setDoctorProfile","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"DoctorLoginInfo","outputs":[{"name":"email","type":"string"},{"name":"password","type":"string"},{"name":"PatOfDocSize","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
unlocked = web3.geth.personal.unlockAccount(web3.eth.coinbase,"1",15000)
contract = web3.eth.contract(address=address,abi=abi)


patient_logged_id = None


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

		unlocked = web3.geth.personal.unlockAccount(web3.eth.coinbase,"1",1500)

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

		unlocked = web3.geth.personal.unlockAccount(web3.eth.coinbase,"1",1500)

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

		unlocked = web3.geth.personal.unlockAccount(web3.eth.coinbase,"1",1500)

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
	count = contract.functions.getInsurerCounter().call()
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
		temp2 = temp2[1:-1]
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

def AddinsToUsr(request):
	csrf_token = get_token(request)
	if request.is_ajax():
		request_data = request.POST
		insid = int(request_data['insid'])
		patid = int(request_data['patid'])

		unlocked = web3.geth.personal.unlockAccount(web3.eth.coinbase,"1",1500)

		if unlocked:
			temp = contract.functions.AddInsToUsr(patid,insid).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
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
		
		fileNamelst = ","

		for img in imglst:
			img = str(img).encode('utf-8')
			hashedWord = sha256(img.strip()).hexdigest()
			imgname = "MedicalRecords/"+str(hashedWord) + str(datetime.datetime.now().timestamp())
			print(imgname)
			fileNamelst =fileNamelst+imgname+","
			with open(imgname, "w") as text_file:
				text_file.write(str(img))

		license = request_data['license']
		unlocked = web3.geth.personal.unlockAccount(web3.eth.coinbase,"1",1500)

		if unlocked:
			temp = contract.functions.AddMedicalRecord(patient_logged_id,disease,fileNamelst,license).transact()
			while web3.eth.getTransaction(temp)['blockNumber'] is None:
				chk = 'do nothing'
			data = json.dumps(dict(web3.eth.getTransaction(temp)),cls=HexJsonEncoder)
			return JsonResponse(data, safe=False)

	return render(request,'index.html')