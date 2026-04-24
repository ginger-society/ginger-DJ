python3 -m build
python3 -m twine upload --repository pypi dist/*  --verbose



export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"