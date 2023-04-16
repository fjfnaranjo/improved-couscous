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
