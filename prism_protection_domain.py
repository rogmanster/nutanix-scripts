import requests
import sys

class RestAPI(object):
	def __init__(self, ip_address, username, password):
		self.ip_address = ip_address
		self.username = username
		self.password = password
		self.base_url = 'https://%s:9440/api/nutanix/v2.0' %self.ip_address
		self.s = requests.Session()
		self.s.auth=(self.username, self.password)
		requests.packages.urllib3.disable_warnings()

	def pd_group(self):
		# List the PD names
		url = self.base_url + '/protection_domains'
		req = self.s.get(url, verify=False)
		resp = req.json()
		
		print('\n**** List of Protection Domains ****\n')
		count = 0
		for x in range(len(resp['entities'])):
			print('{}) {}'.format( count, resp['entities'][x]['name']))
			count += 1

		input_PD = input('\nWhich PD number? ')
		return(resp['entities'][int(input_PD)]['name'])

	def vm_unprotect(self, pd_name):

		# List VMs to remove from PD
		url1 = self.base_url + '/protection_domains/' + str(pd_name)
		req1 = self.s.get(url1, verify=False)
		resp1 = req1.json()

		print('\n\n**** List of Protect VMs ****\n')
		count = 0
		for y in range(len(resp1['vms'])):
			print('{}) {}'.format(count, resp1['vms'][y]['vm_name']))
			count += 1

		input_vm = input('\nWhich VM number to remove? ')

		# Remove the VM from PD
		url2 = self.base_url + '/protection_domains/' + pd_name + '/unprotect_vms/'
		vm_json = [ resp1["vms"][int(input_vm)]["vm_name"] ]
		req2 = self.s.post(url2, json=vm_json, verify=False)
		resp2 = req2.json()
		print("\n***VM Unprotected!!***")
	

	def list_vm_protect(self):
		url = self.base_url + '/protection_domains/unprotected_vms/'

		#Display list of un-protected VMs
		req = self.s.get(url, verify=False)
		resp = req.json()
		print(resp)
		print('\n**** List of Unprotected VMs ****\n')
		count = 0
		for x in range(len(resp['entities'])):
			print('{}) {}'.format(count , resp['entities'][int(x)]['vm_name']))
			count += 1

		input_vm = input('\nEnter number of VM to protect? ')
		return(resp['entities'][int(input_vm)]['vm_name'])

	def vm_protect(self, vm_name, pd_name):
		url = self.base_url + '/protection_domains/' + str(pd_name) + '/protect_vms'

		protect_json = {"names" : [ vm_name ]}
		print(protect_json)
		req = self.s.post(url, json=protect_json, verify=False)
		resp = req.json()
		print(resp)
		print('\n\n***VM Protected!!***\n')


def main():
	test = RestAPI(sys.argv[1],sys.argv[2],sys.argv[3])

	waiting = True
	while waiting:
		user_input = int(input('\nWould you like to (1) Protect or (2) Un-Protect VMs? '))
		if user_input == 1:
			vm_name = test.list_vm_protect()
			pd_name = test.pd_group()
			test.vm_protect(vm_name,pd_name)
			waiting = False
		elif user_input == 2:
			pd_group_name = test.pd_group()
			test.vm_unprotect(pd_group_name)
			waiting = False


if __name__ == "__main__":
	main()