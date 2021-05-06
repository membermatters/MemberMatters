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

```