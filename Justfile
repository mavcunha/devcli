@test *options:
  poetry run pytest {{options}}

@lint:
  poetry run black . --check

@build:
  poetry build --format=wheel

@install: build
  pipx install --force dist/devcli*.whl

@local: build install

@check: install
  devcli template ping
  devcli example ping
  -devcli example version
