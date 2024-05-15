# DNS-Toolbox Demo

This is a simple web application that demonstrates the use of DNS-Toolbox. The App is designed to allow for DNS queries to be made like MXToolbox.com. It can help you solve DNS problems, find out about your DNS records, and more. Another Demo will focus around the check of SSL certificates.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

What things you need to install the software and how to install them:

```sh
pip install -r requirements.txt
```

## Running the App

How to run the streamlit app:

```sh
streamlit run app.py
```

or you can use the docker image:

```sh
docker run -p 8501:8501 -d --name dns-toolbox-demo ghcr.io/hra42/go-dnstoolbox-pythondemo:latest
```

Later I will add a Dockerfile to run the app in a container.

## Built With

* [Streamlit](https://streamlit.io/) - The web framework used
* [Python](https://www.python.org/) - The programming language used
