# rss-parser

## Requirements
* Python = 3.9
* [Docker](https://www.docker.com/)

## Installation

### Docker way

Build Docker image
```sh
$ docker build -t rss:latest .
```

Run Console via Docker
```sh
$ docker run -p 8080:8080 rss:latest .
```

### Local Environment Way

Create virtual environment & activate it
```shell
$ python3.9 -m venv 'venv-example' 
$ source venv-example/bin/activate
```
Install the requirements
```shell
$ pip install -r src/requirements.txt
```
Create db file 
```shell
touch src/rss-parser.db
```

You can run the app programmatically from main.py or with uvicorn.

1.Programmatically, add this to your main.py and run it.
```python
if __name__ == "__main__":
    uvicorn.run("main:app", host="host", port="port", log_level="info")
```
2. Uvicorn 
```shell
uvicorn main:app --reload --host "host" --port "port"
```

### Code Styling

#### Flake8 and Black with pre-commit

1. Installation:
 - with pip
    ```sh
    cd path/to/rss-parser/
    python<version> -m pip install pre-commit
    python<version> -m pre-commit install
    ```
 - with brew on OsX
    ```sh
    cd path/to/rss-parser/
    brew install pre-commit
    pre-commit install
    ```

2. Usage:
 - Just commit :)