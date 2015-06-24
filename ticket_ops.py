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
	subdomain ='https://{}/api/v2/'.format(sub)

def ticket_list(optional_params=[], required_params=[], start_date='', end_date=time.strftime("%Y/%m/%d")):
	""" Return a list of ticket id's who's keys match the optional_params and required_params lists,
		  and the tickets creation date is within the range of start_date and end_date.
		  both optional and required params are lists of 2 element lists, the first element being the key
		  and the second element being the regex you wish to match against the key,
		  Default dates are from the first ticket created to the most recent ticket created.
	"""

	url = subdomain + 'incremental/tickets.json?start_time=0'
	ticket_list = []
	while url:
		response = requests.get(url, auth=(user, pwd))
		response.raise_for_status()

		data = response.json()
		for ticket in data['tickets']:
			if (ticket['created_at'] and ticket['created_at'] >= start_date and ticket['created_at'] <= end_date):
				i = 0
				# Only one key has to match it's regex for this to work
				for param in optional_params:
					if ticket[param[0]] and re.search(param[1], ticket[param[0]]):
						i = 1
				j = 0
				# Every key has to match it's regex for this to work
				for param in required_params:
					if ticket[param[0]] and re.search(param[1], str(ticket[param[0]])):
							j += 1
				if j == len(required_params) and i:
					ticket_list.append(ticket['id'])
					print ticket['id']
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
		try:
			audit_response.raise_for_status()
		except Exception:
			print('Status:', audit_response.status_code, 'Problem with the request for ticket with id {}. Moving on.'.format(ticket_id))

		audit_data = audit_response.json()
		for audit in audit_data['audits']:
			if 'attachments' in audit['events'][0] and audit['events'][0]['attachments']:
				for attachment in audit['events'][0]['attachments']:
					if re.search(regex, attachment['file_name']):
						i = 1
		if i:
			attachment_list.append(ticket)
	return attachment_list

# def _has_attachment(audits, regex):
#       for _ in _get_attachments(audits, regex):
#           return True
#       return False

# def _get_attachments(audits, regex):
#     attachment_list = []
#     for audit in audits:
#         if 'attachments' in audit['events'][0] and audit['events'][0]['attachments']:
#             for attachment in audit['events'][0]['attachments']:
#                 if re.search(regex, attachment['file_name']):
#                     yield attachment['id']

def attachment_list(ticket_id_list, regex='\d|\D'):
	"""	Find a list of attachment id's belonging to a list of tickets(ticket_id_list)
			who's file matches a given regex. Default regex will match everything. """

	attachment_list = []
	for ticket in ticket_id_list:
		audit_url = subdomain + 'tickets/' + str(ticket) + '/audits.json'
		audit_response = requests.get(audit_url, auth=(user,pwd))
		try:
			audit_response.raise_for_status()
		except Exception:
			print('Status:', audit_response.status_code, 'Problem with the request for ticket with id {}. Moving on.'.format(ticket_id))


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
		try:
			remove_ticket_response.raise_for_status()
		except Exception:
			print('Status:', audit_response.status_code, 'Problem with the request for ticket with id {}. Moving on.'.format(ticket_id))









