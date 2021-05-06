# Security group for app running in public subnet

terraform {
  source = "${get_terragrunt_dir()}/../../../modules//sg"
}
dependency "vpc" {
  config_path = "../vpc"
}
include {
  path = find_in_parent_folders()
}

inputs = {
  comp = "app-public"
  ingress_ports = [80, 443]

  vpc_id = dependency.vpc.outputs.vpc_id
}
