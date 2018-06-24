
provider "nutanix" {
  username = "nutanix"
  password = "Nutanix/4u!"     
  endpoint = "10.0.0.101" /* This is the cluster IP you wish to use not prismcentral */
  insecure = true
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
      uuid = "4e521e6c-402f-4b1e-8bd2-a30e764c759f"
      }
    }
  ]

  guest_customization_cloud_init_user_data = "${base64encode("${file("~/Documents/GitHub/huggybear/cloud_config.conf")}")}"

}
