@test *options:
  poetry run pytest {{options}}

@lint:
  poetry run black . --check
