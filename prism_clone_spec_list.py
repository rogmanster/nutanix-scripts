#!/usr/bin/env python3
#  ◤------◥
#  l ● ▄ ● l 
#   l‿/ʊ\‿l
#   l══o══l
#   ︳ ︳︳l⊃
#  'ఋ''ఋ'   
# 	  
# Prism RestAPI Script to demonstrate getting VM list, cloning VM and Power-on
# Execute script using scriptname <ip address of Prism> <username> <password>
# Author: Roger Chao ~ 2017

import sys
import requests
import prism

class RestAPI(object):
	def __init__(self, ip_address, username, password):
		self.ip_address = ip_address
		self.username = username
		self.password = password
		self.s = requests.Session()
		self.s.auth=(self.username, self.password)
		requests.packages.urllib3.disable_warnings()
		self.base_url = 'https://%s:9440/api/nutanix/v2.0' %self.ip_address

	def menu(self):
		user_menu = input("**** User Menu *****: \n\n 1) Clone VM \n\n 2) Delete VM \n\nPlease enter action to perform: ")
		return user_menu

	def clone_vm(self):
		
		# Get List of VMs 
		get_url = self.base_url + '/vms/'
		req = self.s.get(get_url, verify=False)
		resp = req.json()
		list_count = 0
		print("\n**** List of VMs ****\n")
		for x in range(len(resp['entities'])):
			print("{}) {}".format(list_count, resp['entities'][x]['name']))
			list_count += 1
		vm_clone = input("\nPlease enter number of VM to clone: ")
		num_of_clones = int(input("\nPlease enter how many clones: "))

		# Get VM UUID and VM Name
		vm_uuid = resp['entities'][int(vm_clone)]['uuid']
		vm_name = resp['entities'][int(vm_clone)]['name']
		print('\n\nvm_uuid:', vm_uuid)

		# Generate multi-vm Spec_list
		spec_count = 0
		spec_list = { "spec_list": [ ] }
		generate = True
		while generate:

			if num_of_clones != 0:
				spec_count += 1
				spec_list["spec_list"].append({"name": vm_name + '-' + str(spec_count)})
				num_of_clones -= 1

			else:
				generate = False

		# Clone using Spec_list
		clone_url = self.base_url + '/vms/' + vm_uuid + '/clone/'
		#print(clone_url)
		
		req_clone = self.s.post( clone_url, json=spec_list, verify=False )
		resp_clone = req_clone.json()
		return(resp_clone['task_uuid'])

	def poll_task(self, task_uuid):
		
		# Define URL with task_uuid to poll
		url = self.base_url + '/tasks/' + task_uuid + '?include_subtasks_info=true'
		#print(url)

		# Start polling of task until "percentage_complete": 100
		polling = True
		while polling:
			req = self.s.get(url, verify=False)
			resp = req.json()
			if resp['progress_status'] == 'Succeeded':
				polling = False

		# Generate list of entity_ids to power on VM
		self.entity_list = [ resp['entity_list'][x]['entity_id'] for x in range(len(resp['entity_list'])) ]

	# Calling power on function - but passing in a list with variable number of arguments
	def power_on(self):

		poweron = { "transition": "ON" }

		#print("poweron list", self.entity_list)
		for x in self.entity_list:
			url = self.base_url + '/vms/' + x + '/set_power_state/'
			self.s.post( url, json=poweron , verify = False )
			print("working...")
		print("\n\n...DONE!!!")		

	def delete_vm(self):
		pass	

def main():
	test = RestAPI(sys.argv[1], sys.argv[2], sys.argv[3])
	task_uuid = test.clone_vm()	
	print('task uuid:', task_uuid)
	test.poll_task(task_uuid)
	test.power_on()

if __name__ == "__main__":
	sys.argv[:]
	print(sys.argv[:])
	main()



