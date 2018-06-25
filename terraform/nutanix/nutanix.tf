
provider "nutanix" {
  username = "nutanix"
  password = "Nutanix/4u!"     
  endpoint = "10.0.0.102" /* This is the cluster IP you wish to use not prismcentral */
  insecure = true
  port     = 9440
}

resource "nutanix_virtual_machine" "my-machine" {
  #count = "1"
  name  = "tf-vm1"

  num_vcpus_per_socket = "2"
  num_sockets          = "1"
  memory_size_mib      = "512"
  power_state          = "ON"

  nic_list = [
    {
      subnet_reference = {
        kind = "subnet"
        uuid = "d21dedcb-0b7b-4c4d-a3e6-30efe9378817"
      }
    }
  ]

  disk_list = [
    {
      data_source_reference = {
      kind = "image"
      # CentOS7-Base Image from from Image Library - VM UUID 
      uuid = "e0ba6112-0f7d-4d03-bc69-258dedea5a7e"
      }
    }
  ]

  guest_customization_cloud_init_user_data = "${base64encode("${file("~/Documents/GitHub/huggybear/cloud_config.yml")}")}"

}
