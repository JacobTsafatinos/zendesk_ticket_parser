import requests
import re
import time
from os import getenv, environ
import sys
import argparse


class ZendesSearcher(object):
    """
    Simple Zendesk thing.
    """

    def __init__(self, sub_domain='support.waveapps.com'):
        self.url ='https://{}/api/v2/'.format(sub_domain)
        self.auth = requests.auth.HTTPBasicAuth(getenv('ZENDESK_API_USERNAME'), getenv('ZENDESK_API_PASSWORD'))
        self.headers = {'content-type': 'application/json'}

    def get_page_url(self, path):
        return '{}{}'.format(self.url, path)


    def get_matching_tickets(self, optional_params=[], required_params=[], start_date=None, end_date=None):
        """
        Return a list of ticket id's if any of the tickets parameters in the params list
        match the given regex and the tickets creation date is within the range of start_date and end_date.
        Default regex will go match everything, Default dates are from the first ticket created to the
        most recent ticket created.
        """
        url = self.get_page_url('incremental/tickets.json?start_time=0')

        while url:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()

            data = response.json()

            for ticket in data['tickets']:
                created_at = ticket.get('created_at', None)
                created_at = created_at and datetime.strptime(created_at.split('T')[0], '%Y-%m-%d')
                if not (created_at or start_date or end_date) or ((start_date and created_at < start_date) or (end_date and created_at > end_date)):
                    continue

                req_matches_found = [ticket[field] and re.search(pattern, ticket[field]) for field, pattern in required_params.viewitems()]
                ops_matches_found = [ticket[field] and re.search(pattern, ticket[field]) for field, pattern in optional_params.viewitems()]
                if any(ops_matches_found) and all(matches_found):
                    yield ticket['id']

            url = data['next_page']
            if len(data['tickets']) < 1000:
                break

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

		def _has_attachment(audits, regex):
		      for _ in _get_attachments(audits, regex):
		          return True
		      return False

		def _get_attachments(audits, regex):
		    attachment_list = []
		    for audit in audits:
		        if 'attachments' in audit['events'][0] and audit['events'][0]['attachments']:
		            for attachment in audit['events'][0]['attachments']:
		                if re.search(regex, attachment['file_name']):
		                    yield attachment['id']

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









