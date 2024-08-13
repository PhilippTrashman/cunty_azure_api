# Cunty Azure API

The Cunty Azure API is a powerful tool for interacting with with my utmost insanity.  
Its purpose was to to make creating a school planner app easier by moving the Database to central location, as most students didnt know the first thing about api's oder databases
The entire tool was written in a manic episode in a single weekend.  
If the documentation is not written, write it yourself.  

## Features

- SQLAlchemy for Easy Query Writing
- Adapters for managed result outputs
- GREAT error handling ;)  
- Fortnite

## Getting Started

To get started with the Cunty Azure API, follow these steps:

1. Clone the repository: `git clone https://github.com/PhilippTrashman/cunty_azure_api.git` or `git@github.com:PhilippTrashman/cunty_azure_api.git`
2. Create a venv `python -m venv .venv`
3. Install the required dependencies into the venv:

``` bash
    "Linux/MacOS"            "Windows"
. .venv/bin/activate | .venv/Scripts/activate
pip install -m requirements.txt
```

4. setup `local.settings.json`

``` json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "AzureWebJobsStorage": "",
    "TOKEN": {Your Token Here},
    "DATABASE_URL": "postgresql://postgres:1234@localhost:6971/cuntydb"
  }
}
```

5. Run the docker-compose.yaml to generate the postgres databases
6. Run backend.models once to generate the necessary tables
7. Start the api with `func start`

For detailed documentation and usage examples, please refer to the [API Documentation](./docs/api.md).

## Frequently Asked Questions

- __What if i dont want to use PostgreSQL?__

    Then you would have to rewrite the account model to not use PostgresSQL like data.  
    Meaning no UUID's as most dialects dont support these.  
    You would also need to rewrite every adapter that uses the Account model, which can be a pain in the ass, namely:

  - abscence_adapter
  - access_token_adapter
  - acccount_adapter (duh)
  - contact_adapter
  - parent_adapter
  - student_adapter
  - su_adapter
  - teacher_adapter

    just replace uuid with your new datatype. Of course also rewrite the models and refresh the Database

- __What if i still want to use UUID's?__

    Firstly, UUID's are used here just because the have a more uniform look in a url, you could just use them as a String if you really need them.  

- __How can i migrate Datatypes for the Database?__

    You cant :D  

    No but seriously database migration isnt implemented in the API,
    if you want to add more Values to a model or Change Datatypes you need run the `refresh_db` function in `backend.models.py`  
    There are some tools like `Alembic` which can handle Database Migration specifically for SQLAlchemy but i didnt want to work on that.  
    Please implement it if you think its necessary and start a pull request.
