# Zendesk Ticket Parser

This is a script written in Python for the Zendesk API to allow users to find tickets with specific information in them. Included is a method of finding specific attachments associated with those tickets, as well as methods for deleting the tickets. This parser will go through every ticket created.

# Usage

<tt>set_params(usr, password)</tt>
<ul>
<li>usr - the email adress to be used to connect to the Zendesk API</li>
<li>password - a token password for accessing the Zendesk API</li>
</ul>

<tt>url_builder(sub)</tt>
<ul>
<li>sub - the subdomain used in the request url. Example: 'https://(your_subdomain.zendesk.com)/api/v2/groups.json'</li>
</ul>

<tt>ticket_list(optional_params, required_params, start_date, end_date)</tt>:
<ul>
<li>optional_params - a optional list (only one key needs to match the regex to return the ticket id) of 2 element lists. The first element is a key parameter to search through within the ticket object. The second element is a regex to match the key against. Example: ([['subject', 'hello'], ['description', 'monkeys are attacking']])</li>
<li>required_params - same as optional params execpt all keys must match the given regex to return the ticket id</li>
<li>start_date - the first date you want to consider when looking at tickets.</li>
<li>end_date - the last date you want to consider when looking at tickets.</li>
</ul>

<tt>has_attachment(ticket_id_list, regex)</tt>:
<ul>
<li>ticket_id_list - a list of ticket id's that you would like to parse through to find if they have any attachments</li>
<li>regex - a regular expression to find attachments meeting specific file names. For example if you only wanted pdf attachments you could use 'pdf' as your regex argument.</li>
</ul>

<tt>attachment_list(ticket_id_list, regex)</tt>:
<ul>
<li>ticket_id_list - a list of ticket id's that you would like to parse through to find if they have any attachments</li>
<li>regex - a regular expression to find attachments meeting specific file names. For example if you only wanted pdf attachments you could use 'pdf' as your regex argument.</li>
</ul>

<tt>chunks(l, n)</tt>:
<p>This method exists as a way to capatalize on Zendesks bulk remove option for tickets. It can accept up to 100 tickets, sometimes our ticket_list method can return a list with hundreds or thousands of tickets, breaking them up in to 100 element chunks allows us to make less requests in the end.</p>
<ul>
<li>l - a list to break in to smaller sublists</li>
<li>n - the ammount of elements you want in each sublist. The last sublist will contain any leftover elements if they don't perfectly break up in to n element sublists.</li>
</ul>

<tt>delete_tickets(ticket_id_list)</tt>:
<ul>
<li>ticket_id_list - a list of ticket id's for the tickets you wish to delete.</li>
</ul>

#TO DO:

<ul>
<li>Find a way to only search through tickets between specific time intervals, currently we're always going through all tickets no matter what.</li>
<li>Write meaningful tests</li>
</ul>

<!-- <tt>delete_attachments(ticket_id_list)</tt>:
<ul>
<li>attachment_id_list - a list of attachment id's for the attachments you wish to delete.</li>
</ul> -->
