# Deploying Member Matters to the Cloud

## Required tools:

- `terraform`
- `terragrunt`
- `aws-vault` (optional, a nice way to store AWS creds in keyring)

## Step 1: Set env variables and AWS creds

```bash
cd terraform/
aws-vault exec gctechspace-prod -- # note: env creds expire after 30 mins
export ENV=prod
source ./set_env.sh
```

## Step 2: Initial bootstrapping

```bash
# nameservers for the zone we're gonna use in AWS land
terragrunt apply --terragrunt-working-dir membermatters/$ENV/route53-delegation-set
# setup the zone for members.gctechspace.org
terragrunt apply --terragrunt-working-dir membermatters/$ENV/route53-public

# now we have a zone and name servers, we can delegate members.gctechspace.org to AWS from CloudFlare config
# this is done manually through CloudFlare:  "ns-1453.awsdns-53.org", "ns-1914.awsdns-47.co.uk", "ns-217.awsdns-27.com", "ns-797.awsdns-35.net",

# confirm subdomain delegation to AWS worked:
host -t ns members.gctechspace.org
    members.gctechspace.org name server ns-1453.awsdns-53.org.
    members.gctechspace.org name server ns-1914.awsdns-47.co.uk.
    members.gctechspace.org name server ns-217.awsdns-27.com.
    members.gctechspace.org name server ns-797.awsdns-35.net.

# Create AWS SSL cert for *.members.gctechspace.org
terragrunt apply --terragrunt-working-dir membermatters/$ENV/acm-public
# Create VPC for hosting this app in (note down the VPC ID, public and private subnet IDs)
terragrunt apply --terragrunt-working-dir membermatters/$ENV/vpc

# Security groups for our public app and for the DB
terragrunt apply --terragrunt-working-dir membermatters/$ENV/sg-app-public
terragrunt apply --terragrunt-working-dir membermatters/$ENV/sg-db

# Create the DB! get RDS master password from env variable:
source secrets.sh 
terragrunt apply --terragrunt-working-dir membermatters/$ENV/db
```