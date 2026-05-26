#!/usr/bin/python

import csv
import argparse

parser = argparse.ArgumentParser(description="A simple CSV Reader")
parser.add_argument("-f", "--file", required=True, help="CSV file to read")
parser.add_argument("-c", "--columns", type=str, help="Comma-separated column names to display (omit to show all)")
parser.add_argument("-g", "--group-by", type=str, help="Column name to group results by")
args = parser.parse_args()


def read_csv_file(file_path, columns=None, group_by=None):
    with open(file=file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_reader.fieldnames = [f.strip() for f in csv_reader.fieldnames]

        all_columns = csv_reader.fieldnames

        if group_by and group_by not in all_columns:
            print(f"Warning: group-by column '{group_by}' not found in file.")
            print(f"Available columns: {', '.join(all_columns)}")
            return

        if columns:
            selected = [c.strip() for c in columns.split(",")]
            missing = [c for c in selected if c not in all_columns]
            if missing:
                print(f"Warning: columns not found in file: {', '.join(missing)}")
                print(f"Available columns: {', '.join(all_columns)}")
                return
        else:
            selected = all_columns

        if group_by:
            selected = [c for c in selected if c != group_by]

        rows = [row for row in csv_reader if any(row.values())]

    if group_by:
        groups = {}
        for row in rows:
            key = row[group_by]
            groups.setdefault(key, []).append({col: row[col] for col in selected})

        for key, group_rows in groups.items():
            print(f"{group_by}: {key}")
            for row in group_rows:
                for col, val in row.items():
                    print(f"  {col}: {val}")
            print()
    else:
        for row in rows:
            for col in selected:
                print(f"{col}: {row[col]}")
            print()


read_csv_file(args.file, args.columns, args.group_by)
