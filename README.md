# Flask Auth Server and Resource API

**This project is a solution for Exercise 1: Setting up an authorization and authentication flow between a client, authorization server, and resource server.**

This project consists of a Flask authentication server, resource API, and client demo script to simulate the requests and responses between them for authentication and accessing protected resources.

## Overview

The auth server manages user accounts and issuing JWT access tokens. For simplicity, user data is stored in a JSON file instead of a real database.

The resource API verifies access tokens by making a request to the auth server. It serves protected resources to authorized clients.

The client demo script shows how to authenticate with the auth server to get an access token, and use that to access protected resources from the API.

Docker Compose is used to run the auth server and resource API in isolated containers connected on a bridge network to simulate a real deployment.

## Usage

To start the servers with Docker Compose, run:

```
docker-compose up --build -d
```

Then you can execute the demo client script

```
python client/demo.py
```

The client will authenticate with the auth server and retrieve data from the resource API.

## Authentication Flow

The client authenticates with the auth server using a username and password.

The auth server verifies the credentials and issues a signed JWT access token.

The client uses this access token to make requests to the protected resource API. 

The resource API verifies the access token signature by making a request to the auth server before returning any protected resources.

## Security

Passwords are hashed with MD5 before storing in the auth server's simple JSON file database. This should be upgraded to a real database in production.

JWT access tokens are signed with a secret key to prevent tampering.

The resource API only accepts token validation requests from allowed hosts.

## Next Steps

This demonstrates a simple but complete authentication flow with Flask.

Next steps could include:

- Using a real database like PostgreSQL, MySQL or NoSQL like Firebase for data persistence instead of a JSON file.

- Building out a frontend UI for authentication and accessing the resource API instead of the demo client script.

- Deploying the servers and UI to a cloud provider.