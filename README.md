# improved-couscous
A simple reference implementation for a birthday greeter API.

This project uses a self-contained Python 3 environment inside a Docker image
to normalize the development environment.

The proper commands to manage this environment and interact with the project
can be issue by simple Make invocations.

## Create the Docker image

```
make image
```

## Run the tests

```
make test
```

## Deploy the API

```
export AWS_DEFAULT_REGION="region"
export AWS_ACCESS_KEY_ID="id"
export AWS_SECRET_ACCESS_KEY="secret"
make deploy
```

## GitHub actions
There are two GitHub actions configured to handle the CI/CD. One of them checks
the code for quality and runs the tests. The other one deploys the code to
production (this one, only when GitHub releases are created).

The deployment action uses GitHub secrets to provide Zappa with a credential to
update the AWS function. The secrets are the 3 environment variables used by
the AWS tooling.
