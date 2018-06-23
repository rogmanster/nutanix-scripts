provider "nutanix" {
  username = "nutanix"
  password = "Nutanix/4u!"
  endpoint = "10.0.0.101"
  insecure = true
  port     = 9440
}

resource "nutanix_virtual_machine" "my-machine" {
  metadata {
    kind = "vm"
    name = "metadata-name-test-dou-%d"
  }

  name = "name-test-dou-%d"

  cluster_reference = {
    kind = "cluster"
    uuid = "00056eda-31fe-0b6a-336d-001fc69be30e"
  }

  num_vcpus_per_socket = 1
  num_sockets          = 1
  memory_size_mib      = 512
  power_state          = "ON"

  nic_list = [{
    nic_type = "NORMAL_NIC"

    subnet_reference = {
      kind = "subnet"
      uuid = "d21dedcb-0b7b-4c4d-a3e6-30efe9378817"
    }

    network_function_nic_type = "INGRESS"
  }]

  disk_list = [
    {
      data_source_reference = [{
        kind = "image"
        name = "Centos7"
        uuid = "a866d321-b892-44c2-b7f8-12c8f0a8d33e"
      }]

      device_properties = [{
        device_type = "DISK"
      }]

      disk_size_mib = 1
    },
  ]

output "ip" {
  value = "${nutanix_virtual_machine.my-machine.ip_address}"
}
