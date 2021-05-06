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
```