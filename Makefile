bin = .venv/bin

make:
	$(bin)/python -m blog content/ .

clean:
	rm -rf site

serve:
	$(bin)/python -m http.server -d site/ 5000

format:
	$(bin)/black src tests
	$(bin)/isort src tests

lint:
	$(bin)/mypy src tests

test:
	$(bin)/pytest

verify: lint test
