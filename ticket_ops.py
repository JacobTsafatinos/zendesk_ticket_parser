import requests
import re
import time

def set_params(usr, password):
	"""Initializes the user, password and subdomain strings to be used in all our API requests"""

	global user
	global pwd
	user = usr
	pwd = password

def url_builder(sub):
	"""Create the beggining string to every request url"""

	global subdomain
	subdomain = 'https://' + sub + '/api/v2/'

def ticket_list(params, start_date='', end_date=time.strftime("%Y/%m/%d")):
	""" Return a list of ticket id's if any of the tickets parameters in the params list
		  match the given regex and the tickets creation date is within the range of start_date and end_date.
		  Default regex will go match everything, Default dates are from the first ticket created to the
		  most recent ticket created.
	"""

	url = subdomain + 'incremental/tickets.json?start_time=0'
	ticket_list = []
	while url:
		response = requests.get(url, auth=(user, pwd))
		# Check for HTTP codes other than 200
		if response.status_code != 200:
			print('Status:', response.status_code, 'Problem with the request. Exiting.')
			exit()
		data = response.json()
		for ticket in data['tickets']:
			if (ticket['created_at'] and ticket['created_at'] >= start_date and ticket['created_at'] <= end_date):
				i = 0
				for param in params:
					if (ticket[param[0]] and re.search(param[1], ticket[param[0]])):
						i = 1
				if i:
					ticket_list.append(ticket['id'])
		url = data['next_page']
		if len(data['tickets']) < 1000:
			break
	return ticket_list

def exact_ticket_list(params, start_date='', end_date=time.strftime("%Y/%m/%d")):
	""" Return a list of ticket id's if any of the tickets parameters in the params list
		  match the given regex and the tickets creation date is within the range of start_date and end_date.
		  Default regex will go match everything, Default dates are from the first ticket created to the
		  most recent ticket created.
	"""

	url = subdomain + 'incremental/tickets.json?start_time=0'
	ticket_list = []
	while url:
		response = requests.get(url, auth=(user, pwd))
		# Check for HTTP codes other than 200
		if response.status_code != 200:
			print('Status:', response.status_code, 'Problem with the request. Exiting.')
			exit()
		data = response.json()
		for ticket in data['tickets']:
			if (ticket['created_at'] and ticket['created_at'] >= start_date and ticket['created_at'] <= end_date):
				i = 0
				for param in params:
					if ticket[param[0]]:
						if re.search(param[1], str(ticket[param[0]])):
							i += 1
					else:
						i += 1
				if i == len(params):
					ticket_list.append(ticket['id'])
		url = data['next_page']
		if len(data['tickets']) < 1000:
			break
	return ticket_list

def has_attachment(ticket_id_list, regex='\d\D'):
	"""	Find a list of ticket id's that have attachments
			who's file matches a given regex. Default regex will match everything. """

	attachment_list = []
	for ticket in ticket_id_list:
		i = 0
		audit_url = subdomain + 'tickets/' + str(ticket) + '/audits.json'
		audit_response = requests.get(audit_url, auth=(user,pwd))
		# Check for HTTP codes other than 200
		if audit_response.status_code != 200:
		    print('Status:', audit_response.status_code, 'Problem with the request. Moving on.')
		    continue

		audit_data = audit_response.json()
		for audit in audit_data['audits']:
			if 'attachments' in audit['events'][0] and audit['events'][0]['attachments']:
				for attachment in audit['events'][0]['attachments']:
					if re.search(regex, attachment['file_name']):
						i = 1
		if i:
			attachment_list.append(ticket)
	return attachment_list

def attachment_list(ticket_id_list, regex='\d|\D'):
	"""	Find a list of attachment id's belonging to a list of tickets(ticket_id_list)
			who's file matches a given regex. Default regex will match everything. """

	attachment_list = []
	for ticket in ticket_id_list:
		audit_url = subdomain + 'tickets/' + str(ticket) + '/audits.json'
		audit_response = requests.get(audit_url, auth=(user,pwd))
		# Check for HTTP codes other than 200
		if audit_response.status_code != 200:
		    print('Status:', audit_response.status_code, 'Problem with the request. Moving on.')
		    continue

		audit_data = audit_response.json()
		for audit in audit_data['audits']:
			if 'attachments' in audit['events'][0] and audit['events'][0]['attachments']:
				for attachment in audit['events'][0]['attachments']:
					if re.search(regex, attachment['file_name']):
						attachment_list.append(attachment['id'])
	return attachment_list

def chunks(l, n):
		"""break list l in to a list of it's chunks of size n"""

		n = max(1, n)
		return [l[i:i + n] for i in range(0, len(l), n)]

def delete_tickets(ticket_id_list):
	"""Given a ticket_id_list, remove all the ticket's in the list"""

	remove_list = chunks(ticket_id_list, 100)
	for sublist in remove_list:
		ticket_url = subdomain + 'tickets/destroy_many.json?ids=' + str(sublist).strip('[]')
		remove_ticket_response = requests.delete(ticket_url, auth=(user,pwd))
		if remove_ticket_response.status_code != 200:
		    print('Status:', audit_response.status_code, 'Problem with the request. Moving on.')
		    continue

# def delete_attachments(attachment_id_list):
# 	"""Given an attachment_id_list, remove all the ticket's in the list"""
# 	for attachment in attachment_id_list:
# 		attachment_url = subdomain + 'attachments/' + str(attachment) +'.json'
# 		remove_attachment_response = requests.delete(attachment_url, auth=(user,pwd))
# 		if remove_attachment_response.status_code != 200:
# 		    print('Status:', audit_response.status_code, 'Problem with the request. Moving on.')
# 		    continue











