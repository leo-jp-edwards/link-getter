# link-getter

## How to Run

The app can be run and tested locally through the make file. 

Endpoint documentation can be found at http://localhost:8004/docs

> `make build` - Build the docker images necessary and create the DB tables

> `make up` - After building the docker images the project can be run using up

> `make test` - Run all unit / integration tests

> `make coverage` - Create test coverage report

> `make lint_black` - Lint the project using flake8, black and isort

> `make clean` - Remove all pycache etc

> `make down` - Bring down the docker images


## Missing bits

Due to time constraints certain aspects of this project are missing.

- The CI/CD is incomplete
- Terraform infrastructure has not been completed
- End to End tests are not implemented
- Database migration is not implemented - the db is rebuilt locally each time which would be unacceptable in prod
