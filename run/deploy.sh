python3 -m pip install --upgrade pip;
python3 -m pip install --upgrade build;
python3 -m pip install twine;
python3 -m pip install wheel;
python3 setup.py sdist bdist_wheel;
python -m twine upload dist/*;
