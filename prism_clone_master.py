#!/usr/bin/env python3
#  ◤------◥
#  l ● ▄ ● l 
#   l‿/ʊ\‿l
#   l══o══l
#   ︳ ︳︳l⊃
#  'ఋ''ఋ'   
# 	  
# Prism RestAPI Script to demonstrate Get (vm_list), Post (cloning vm) and Delete
# Execute script using scriptname <ip address of Prism> <username> <password>

import requests
import json
import sys
import warnings

class PrismAPI(object):

	def __init__(self, ip_address, username, password):
		# Supress warning for certificate verification from verify=False
		warnings.filterwarnings("ignore")
		self.ip_address = ip_address
		self.username = username
		self.password = password
		base_url = 'https://%s:9440/api/nutanix/v2.0' % self.ip_address
		self.base_url = base_url
		s = requests.Session()
		s.auth = (self.username, self.password)
		self.s = s
		

	def get_list(self, list_title):

		# Requests get list of  VM names 
		url = self.base_url + '/vms/'
		req = self.s.get(url, verify=False) 
		resp = req.json()
		vm_list = []

		# Create list of VM for user input of VM to clone -> identify UUID
		for x in range(len(resp['entities'])):
			vm_list.append(resp['entities'][x]['name'])

		list_out = [x for x in (enumerate(vm_list))]

		# Display list of VM to choose on seperate lines
		print('\n*** List of VMs to {} ***'.format(list_title))
		for x in list_out:
			print ('\n',x)

		# Get the VM UUID to clone
		vm_pick = input("\nPlease enter number of VM: ")
		self.vm_pick = vm_pick
		vm_uuid = resp['entities'][int(vm_pick)]['uuid']
		self.vm_uuid = vm_uuid
		print(self.vm_uuid)

	def clone(self):

		url = self.base_url + '/vms/' + self.vm_uuid + '/clone'
		vm_name = input("\nPlease give clone a name: ")
		self.vm_name = vm_name

		# Clone and Customize Demo - Hostname and IP JSON 
		data = {
			'spec_list': [{
				'memory_mb': 512, 
				'name': vm_name, 
				'num_cores_per_vcpu': 1, 
				'num_vcpus': 1, 
				'override_network_config': 'true', 
				'vm_nics': [{
					'network_uuid': '38c3b3be-1b70-4605-b9af-00c2341bfc85'
				}]
			}], 
			'storage_container_uuid': '4fc5d27c-4d90-4b99-a714-d968f3d3dc45', 
			'vm_customization_config': {
				'datasource_type': 'CONFIG_DRIVE_V2', 
				'userdata_path': 'adsf:///ImageConfigurations/cloud-init-hostandip.yaml'
			}
		}

		# Clone Demo  - No Hostname or IP - JSON
		data1 = {
			'spec_list': [{
				'memory_mb': 512, 
				'name': vm_name, 
				'num_cores_per_vcpu': 1, 
				'num_vcpus': 1, 
				'override_network_config': 'true', 
				'vm_nics': [{
					'network_uuid': '38c3b3be-1b70-4605-b9af-00c2341bfc85'
				}]
			}]
		}
		

		# Figure out which JSON to pass for customize or not customize
		json_config = ""
		vm_customize = input('\nWould you like to customize with Hostname and IP (yes or no)? ')
		if vm_customize == 'yes':
			json_config = data
		else:
			json_config = data1

		vm_clone = self.s.post(url, json=json_config, verify=False)
		resp = vm_clone.json()
		return resp['task_uuid']

	def poll_task(self, task_uuid):

		self.task_uuid = task_uuid
		print(self.task_uuid)
		url = self.base_url + '/tasks/' + self.task_uuid
		clone_in_progress = True

		while clone_in_progress:
			poll_task = self.s.get(url, verify=False)
			resp = poll_task.json()

			if resp['percentage_complete'] == 100 and resp['progress_status'] == 'Succeeded':
				print ('\nSuccess! - cloning complete...')
				clone_in_progress = False

		
	def power_on(self):

		# Requests get list of  VM names to find UUID of VM to power on
		url = self.base_url + '/vms/'
		req = self.s.get(url, verify=False) 
		resp = req.json()
		data = {'transition': 'ON'}

		for x in range(len(resp['entities'])):
			if resp['entities'][x]['name'] == self.vm_name:
				vm_uuid = resp['entities'][x]['uuid']

				# Requests parameters to power on VM
				url_on = self.base_url + '/vms/' + vm_uuid + '/set_power_state/'
				
				# Power on VM from UUID
				vm_power = self.s.post(url_on, json=data, verify=False)
				print ('\nPowering on vm....',self.vm_name)
				resp_power = vm_power.json()
				print (resp_power)

	def vm_delete(self):

		# Call Get List VM Function with Title 'Delete'
		self.get_list('Delete')
		url = self.base_url + '/vms/' + self.vm_uuid
		vm_delete = self.s.delete(url, verify=False)
		resp_delete = vm_delete.json()
		print ('\nSuccess! - deleting complete...\n')
		print (resp_delete)

def main():
	ip_address = sys.argv[1]
	username = sys.argv[2]
	password = sys.argv[3]
	test = PrismAPI(ip_address,username,password)
	test.get_list('Clone')
	task_uuid = test.clone()
	poll = test.poll_task(task_uuid)
	test.power_on()
	test.vm_delete()

if __name__ == "__main__":
	sys.argv[:]
	main()
