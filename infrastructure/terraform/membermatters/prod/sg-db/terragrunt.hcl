# Security group for RDS db

terraform {
  source = "${get_terragrunt_dir()}/../../../modules//sg"
}
dependency "vpc" {
  config_path = "../vpc"
}
dependencies {
  paths = [
    "../sg-app-public",
  ]
}
include {
  path = find_in_parent_folders()
}

inputs = {
  comp = "db"
  name = "membermatters-db"
  app_ports = [3306]
  app_sources = [
    "sg-app-public",
  ]

  vpc_id = dependency.vpc.outputs.vpc_id
}
