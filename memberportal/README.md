# Getting started (Django backend)

First, install uv from [here](https://docs.astral.sh/uv/getting-started/installation/). uv will install and manage
both Python itself and the Python packages we depend on.

Then, grab a copy of this repository and run the commands below _from within this folder_.

## Running the dev server

In production, we have an nginx reverse proxy setup. For development however, it's useful to use the built in
development server. First we need to make sure we have a local sqlite database with the correct migrations applied, and default database.

You probably won't be able to create a log file and database in the default location. You should set a couple of
environment variables like below to create them locally when developing:

To run the Django database migrations:

```bash
MM_LOG_LOCATION=errors.log MM_DB_LOCATION=db.sqlite3 uv run manage migrate
```

After running that you should see something like this:

```bash
Operations to perform:
  Apply all migrations: access, admin, auth, causes, contenttypes, profile, sessions, memberbucks
Running migrations:
  Applying causes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

Now load some initial data into the database:

```bash
MM_LOG_LOCATION=errors.log MM_DB_LOCATION=db.sqlite3 uv run manage loaddata fixtures/initial.json
```

If that completes with no errors (warnings are ok) run the command below to start the development server.

```bash
MM_LOG_LOCATION=errors.log MM_DB_LOCATION=db.sqlite3 uv run manage runserver
```

You should see something like this:

```bash
Django version 2.0.7, using settings 'membermatters.settings'
Starting development server at http://127.0.0.1:8000/
```

Now that the backend API is running, you can head over to the [frontend](/frontend) folder and follow those instructions to get the frontend UI running.

## Stripe Webhooks
If you want to test Stripe webhooks you can use the stripe CLI to forward webhooks to your local dev server.
To do so, you will need to install the stripe CLI and login to your stripe account.
Click [here](https://dashboard.stripe.com/test/webhooks/create?endpoint_location=local) for detailed instructions from
Stripe.

Once you're set up, run the following command to forward webhooks to your local dev server:

```bash
stripe listen --skip-verify --events invoice.paid,invoice.payment_failed,customer.subscription.deleted --forward-to localhost:8080/api/billing/stripe-webhook/
```

Finally, check that you're running the frontend proxy on port 8080 and configure the signing secret in the Constance
settings.
You can find the local signing secret in the command line output after running `stripe listen` above.
It will start like this `whsec_...`

You can also trigger common events like `invoice.paid` using the CLI like this:
```bash
stripe trigger invoice.paid
```

## Linter

As explained below, this projects uses a linter (called "Black") to fix common errors, and to enforce consistent code style/standards.

You can manually run the black linter with the following command in this folder: `black . `

Note that the command above will automatically try to correct any issues that are detected. If you just want to check
your code without automatically applying fixes, you can use: `black --check .`

Failure to ensure your code is compliant with our code formatting and linting standards may result
in rejection of your pull request so please make sure you complete this step.

# Contributing Guidelines

Please use best practices while contributing. This includes writing clean code (messy/hacky
code will be rejected) and making sure it's well commented. Try to think of the next person who comes along so use
variable names that make sense and avoid weird tricks that not everyone will understand.

Please work on existing issues (use comments to clarify/discuss things). If you want to fix undocumented
bugs or add new things, then open an issue for discussion.

Once you are happy with your changes, please open a pull request to merge them into dev. Your changes will be reviewed
and accepted/rejected.

Note to collaborators with push permission: Do not push directly to master. You should push all changes to a feature
branch first (`feature/<feature_name>`). When you are happy with it submit a pull request for merging into main. We use
tags to manage versions, so `main` contains the latest "development" version, and this is tagged when a new
version is released.

We use eslint, prettier and black for code linting and formatting. These are set up as pre-commit
hooks. These are a requirement and anything that fails these rules may not be accepted. If you
would like to suggest changes to the eslint config please open an issue. If you have a specific use
case, you may disable eslint rules on a line by line basis. Any global disables will be rejected
unless you have a good reason.

# Notes

You will need to re-run the database migration every time the db models change. You may see random database related errors such as column does not exist if you forget to do this. You can do that by running:

`MM_LOG_LOCATION=errors.log MM_DB_LOCATION=db.sqlite3 uv run manage migrate`
