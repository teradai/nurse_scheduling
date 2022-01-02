
.PHONY: format
format: 
	isort schedule_creator tests
	black schedule_creator tests

.PHONY: exec
exec:
	python -m schedule_creator.main sample1/shift_request.csv result/result_shift.csv

.PHONY: test
test:
	python -m pytest tests
