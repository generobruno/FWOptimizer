# FWOptimizer

## Developing and Testing

Se debe crear el virtual enviroment, activarlo e instalar las dependencias del pyproject.toml:

``` bash
> python -m venv .venv_name

# Linux
> source .venv_name/bin/activate
# Windows
> .\.venv_name\Scripts\activate

(.venv_name) > pip install -e .
```

Además, para correr los tests se deben instalar las dependecias correspondientes:

``` bash
(.venv_name) > pip install .[test]
```
