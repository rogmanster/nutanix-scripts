provider "nutanix" {
  username = "nutanix"
  password = "Nutanix/4u!"
  endpoint = "10.0.0.101"
  insecure = true
  port     = 9440
}

data "nutanix_clusters" "clusters" {
  metadata = {
    length = 2
  }
}

resource "nutanix_virtual_machine" "vm1" {
  name = "test-dou-update-15"

  description = "test update 4"

  cluster_reference = {
    kind = "cluster"
    uuid = "${data.nutanix_clusters.clusters.entities.0.metadata.uuid}"
  }

  num_vcpus_per_socket = 1
  num_sockets          = 1
  memory_size_mib      = 512
  power_state          = "ON"

  nic_list = [
   {
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
    }
  }

output "ip" {
  value = "${nutanix_virtual_machine.my-machine.ip_address}"
}
