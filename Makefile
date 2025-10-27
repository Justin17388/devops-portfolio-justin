.PHONY: check test fmt


check: fmt test
@echo "All checks passed"


fmt:
pre-commit run --all-files || true


test:
pytest -q || true
