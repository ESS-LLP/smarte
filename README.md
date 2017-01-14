#Smarte

Modules on frappe to suite General Practice, Hospital and Laboratory Management. It is designed to work seamlessly with ERPNext so that healthcare providers can administer their day today operations in a smarter way.

##Installation
	You will need a frappe site with erpnext installed. Visit https://github.com/frappe/bench

		bench get-app smarte https://github.com/ESS-LLP/smarte.git
		bench new-site site.name
		bench --site site.name install-app erpnext
		bench --site site.name install-app smarte

##Demo and Website
		Visit smarteCare(https://smarteHIS.com) to see live demo

##Feature list
####General Practice / Clinic Out Patient
	Appointments scheduling
	Consultation - Prescriptions, Investigations etc.

####Laboratory Management
	Lab Procedures
	Lab Test Result Templates and Printing / Emailing
	Sample Collection
	Configurable workflow - Auto create sample collection task and lab procedure on Invoice submit

####Hospital / In-patient Management(beta)
	In-patient admission, facility allotment
	In-patient treatment plans, progress monitoring
	Infrastructure management - Wards, Rooms, Beds
	Service Units - Nurses’ stations, Diagnostic test centres, Housekeeping units etc. and user assignment
	Service Tasks (Tasks for service units)
	Configurable workflow - Auto create service tasks

####General
	Send SMS - automatic / manual
	Resource Scheduling (Physicians, Service Units etc.)

####License
GNU / General Public License v3.
