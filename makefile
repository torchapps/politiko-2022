.PHONY: dev
dev: data.js
	python3 -m http.server
data.js: cands.csv issues.csv stances.csv sources.csv csv_to_data.py
	python3 csv_to_data.py
