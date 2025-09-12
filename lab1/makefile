run-tests:
	PYTHONPATH=. pytest -v

run:
	python3 run_lab.py --search $(s)


STRIP_ANSI = sed -E 's/\x1b\[[0-9;]*m//g'
EXTRACT    = sed -En 's/.*Needed[[:space:]]+([0-9.]+).*PathLength:[[:space:]]+([0-9]+).*NumExpNodes:[[:space:]]+([0-9]+).*/\1 \2 \3/p'
AVG        = awk '{s1+=$$1; s2+=$$2; s3+=$$3; n++} END{if(n){printf "Avg Needed(msec): %.3f\nAvg PathLength: %.3f\nAvg NumExpNodes: %.3f\n", s1/n, s2/n, s3/n} else {print "No lines found"}}'

perf:
	@python3 run_lab.py --search $(s) --no-gui | $(STRIP_ANSI) | $(EXTRACT) | $(AVG)