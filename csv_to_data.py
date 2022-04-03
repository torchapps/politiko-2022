#!/usr/bin/python3
import csv
import json

datasets = ["cands", "issues", "sources", "stances"]
data_tables = {}
for dataset in datasets:
    with open(f"{dataset}.csv") as f:
        reader = csv.DictReader(f)
        data_tables[dataset] = [x for x in reader]


def get_positions():
    cand_positions = [cand["pos"] for cand in data_tables["cands"]]
    return sorted(set(cand_positions))


def get_cands(position):
    return [cand for cand in data_tables["cands"] if cand["pos"] == position]


def get_issues():
    return data_tables["issues"]


def get_stance(cand, issue):
    for stance in data_tables["stances"]:
        if stance["name"] == cand:
            return stance[issue]


def get_source(cand, issue):
    for source in data_tables["sources"]:
        if source["name"] == cand:
            return source[issue]


data_json = {
    position: {
        cand["name"]: {
            issue["name"]: [
                get_stance(cand["name"], issue["name"]),
                get_source(cand["name"], issue["name"])
            ] for issue in get_issues()
        } for cand in get_cands(position)
    } for position in get_positions()
}


def clear_screen():
    print(chr(27) + '[2j')
    print('\033c')
    print('\x1bc')


with open("data.js", "w+") as f:

    data_contents = f"var data = {json.dumps(data_json, indent=4)}"
    issue_contents = f"var issues = {json.dumps(data_tables['issues'], indent=4)}"

    clear_screen()

    print(data_contents)
    print(issue_contents)

    f.write(data_contents)
    f.write("\n")
    f.write(issue_contents)
