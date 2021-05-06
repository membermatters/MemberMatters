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
# secrets for one time RDS etc.. creation 
source secrets.sh 
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


```