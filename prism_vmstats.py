# v1 API to display CPU usage for a VM

import sys
import requests
import prism_auth

class RestAPI(object):
	def __init__(self, ip_address, username, password):
		self.ip_address = ip_address
		self.username = username
		self.password = password
		self.base_url = 'https://%s:9440/PrismGateway/services/rest/v1/' %self.ip_address
		self.s = requests.Session()
		self.s.auth=(self.username,self.password)
		requests.packages.urllib3.disable_warnings()

	def get_vmstats(self):
		url = self.base_url + 'vms/'
		req = self.s.get(url, verify=False)
		resp = req.json()
		# iterate through vmstat output
		print('{0:25}    {1:8}   {2:5}   {3:5}'.format('VM Name', 'CPU Usage', 'Mem Usage',  'VM UUID'))
		print('-' *78)
		for x in range(len(resp['entities'])):
			print('{0:25}    {1:8}    {2:8}    {3:25}'.format( resp['entities'][x]['vmName'], 
				int(resp['entities'][x]['stats']['hypervisor_cpu_usage_ppm'])/10000,
				int(resp['entities'][x]['stats']['memory_usage_ppm'])/10000,
				resp['entities'][x]['uuid']))
		return (resp)

def main():
	test = RestAPI(sys.argv[1],sys.argv[2],sys.argv[3])
	get_vmstats = test.get_vmstats()

if __name__ == "__main__":
	sys.argv[:]
	main()