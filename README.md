# mini-rag

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.8 or later

### Install Python using Miniconda

1) Download and install Miniconda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)

2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the environment:
```
$ conda activate mini-rag
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r requirments.txt
```

### setup the environment variables
```bash
$ cp .env.example .env
```

Setup your enivronment in `.env` file like SECRET_KEY value


## run the fastapi server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

