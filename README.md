# Zendesk Ticket Parser

This is a script written in Python for the Zendesk API to allow users to find tickets with specific information in them. Included is a method of finding specific attachments associated with those tickets, as well as methods for deleting the tickets and attachments. This parser will go through every ticket created.

# Usage

<tt>set_params(usr, password)</tt>
	usr - the email adress to be used to connect to the Zendesk API
	password - a token password for accessing the Zendesk API

<tt>url_builder(sub)</tt>
	sub - the subdomain used in the request url. Example: 'https://(your_subdomain.zendesk.com)/api/v2/groups.json'

<tt>ticket_list(params, search, regex, start_date, end_date)</tt>:
	params - a list of key parameters to search through within the ticket object. Example: (['subject', 'description']) will search through the values asociated with the subject and description keys.
	regex - a regular expression to match against the values of the params keys given.
	start_date - the first date you want to consider when looking at tickets.
	end_date - the last date you want to consider when looking at tickets.

<tt>attachment_list(ticket_id_list, regex)</tt>:
  ticket_id_list - a list of ticket id's that you would like to parse through to find if they have any attachments
  regex - a regular expression to find attachments meeting specific file names. For example if you only wanted pdf attachments you could use 'pdf' as your regex argument.

<tt>chunks(l, n)</tt>:
	This method exists as a way to capatalize on Zendesks bulk remove option for tickets. It can accept up to 100 tickets, sometimes our ticket_list method can return a list with hundreds or thousands of tickets, breaking them up in to 100 element chunks allows us to make less requests in the end.
  l - a list to break in to smaller sublists
  n - the ammount of elements you want in each sublist. The last sublist will contain any leftover elements if they don't perfectly break up in to n element sublists.

<tt>delete_tickets(ticket_id_list)</tt>:
	ticket_id_list - a list of ticket id's for the tickets you wish to delete.

<tt>delete_attachments(ticket_id_list)</tt>:
	attachment_id_list - a list of attachment id's for the attachments you wish to delete.