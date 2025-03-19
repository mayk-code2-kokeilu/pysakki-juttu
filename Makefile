
myenv:
	python3 -m venv $@

deps: myenv
	./myenv/bin/pip install -r requirements.txt
	touch $@

run: deps myenv
	./myenv/bin/flask --app main run --debug

ipy: deps myenv
	./myenv/bin/ipython

