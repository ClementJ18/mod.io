
pytest --log-level="INFO" --html=report.html -vv --showlocals --cov=modio --cov-report term-missing --self-contained-html "$@"