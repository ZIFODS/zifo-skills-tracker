# Zifo Skills Graph

Zifo Skills Graph is currently in development but is expected to be a full-stack web application that allows the user to visualise and query the skills of Zifo employees. Understanding the skills that employees possess will aid the company with resource allocation and training organisation.

## Getting started

Launching the API will first require Python version 3.10 to be installed.

Once Python is installed, enter the following commands to launch the API:

`python3.10 -m pip install pipenv`
`python3.10 -m pipenv install`
`python3.10 -m pipenv run server`

To be able to visualise the d3 graph network, you'll first need to install `npm` and then use `npm install -g http-server`.

Following install, simply execute `http-server -c-1 frontend` to view the network.