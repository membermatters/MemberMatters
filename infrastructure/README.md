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

## Step 2: Initial bootstrapping of hosted zone / vpc / wildcard ssl certificate

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
```

# Initial setup of app & database

```bash
cd copilot
# Bootstrap copilot setup
copilot app init mm --domain members.gctechspace.org
# Tell copilot to start a "prod" environment in the VPC / security groups we made above
copilot env init -n prod --import-vpc-id vpc-0903228a2ce58d9f2 --import-public-subnets subnet-09e0cd5ec6c42a3e1,subnet-01c831b1e7051d803 --import-private-subnets subnet-050236b57beb46fd0,subnet-0e7676e504a766e50
# Tell copilot to launch a service called "frontend" based on a Dockerfile
copilot svc init --name frontend --svc-type "Load Balanced Web Service" --dockerfile ../../test/Dockerfile
# deploy and start the service
copilot svc deploy

# We now have an app at frontend.prod.mm.members.gctechspace.org - phew! 
# Manually fix up the hostname in AWS console
# 1. Load balancers -> HTTPS Listener -> Change certificate to `members.gctechspace.org`
# 2. Load balancers -> HTTPS Listener -> View/edit rules -> Change hostname to `members.gctechspace.org`
# 3. Load balancers -> HTTP Listener -> View/edit rules -> Change hostname to `members.gctechspace.org`
# These settings should stay as long as we don't delete the app and re-create it.

# Create the database configuration ( enter initial database name as "mm" )
copilot storage init -n mm-db -t Aurora -w frontend --engine MySQL
# Deploy database config and kick of DB creation:
copilot deploy --name frontend 

# Create codedeploy pipeline
copilot pipeline init
# Have a look at the generated files, tweak as needed and add them to git:
git add buildspec.yml pipeline.yml 
# Deploy the pipeline
copilot pipeline update
# Follow the prompts ^^ to connect github up to codepipeline
```

# Manual deploy app

```bash
copilot svc deploy
```

# Connect to running instance

```bash
copilot svc exec --name frontend --env prod -c /bin/bash
```