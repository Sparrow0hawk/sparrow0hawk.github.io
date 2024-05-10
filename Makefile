make:
	.venv/bin/python generate.py
	npm run build

clean:
	rm -rf site

serve:
	python -m http.server -d site/ 8000