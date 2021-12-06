# TeamCity Framework Automation 

Home project to test basic and main functionality of TeamCity CI/CD server.

## Procedure:
## 1. Install all dependencies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```
In order to run UI tests please install browsers with
```bash
playwright install
```

## 2. Usage
Inside the project simply run
```bash
pytest tests
```

## 3. Test results
Test results could be found in GH Actions Workflow. Check the latest green build. 

Local run: 
```python
================================================================================= test session starts ==================================================================================
platform darwin -- Python 3.8.9, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /Users/maringo/PycharmProjects/JetBrains
plugins: anyio-3.4.0
collected 6 items                                                                                                                                                                      

tests/api/test_suite_api.py ...                                                                                                                                                  [ 50%]
tests/ui/test_suite_ui.py ...                                                                                                                                                    [100%]

================================================================================== 6 passed in 38.08s ==================================================================================
```
## License
[MIT](https://choosealicense.com/licenses/mit/)