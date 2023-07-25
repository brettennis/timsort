
run-timsort:
	python3 angularsort.py $(output-info) $(input) $(output-sorted)

run:
	python3 angularsort.py out-info.txt input-points.txt out-sorted.txt