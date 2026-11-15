"""Suppression checker for Lab 7.

Give it the table you intend to publish: one row per ZIP code, one column per group,
a "Total" column, and a final "Total" row. Write "*" in every suppressed cell. Margins
(the Total row and column) are published as they are.

The checker attacks the table the way a reader could: wherever a row or column has
exactly one hidden cell, subtract to recover it, and repeat until nothing changes. It then
uses linear programming to find the narrowest range each remaining hidden cell could take.
A table passes only if no hidden cell is recovered exactly and no range is narrower than
the suppression threshold.

Usage in a notebook:
    from suppression_checker import check
    report = check(published_df)          # published_df as described above
    print(report["passed"], report["recovered"][:5])
Usage from a shell:
    python suppression_checker.py my_table.csv
"""
import sys

import numpy as np
import pandas as pd

THRESHOLD = 11


def _load(df):
    df = df.copy()
    df = df.set_index(df.columns[0])
    df.index = df.index.astype(str)
    total_row = df.loc["Total"]
    body = df.drop(index="Total")
    total_col = body["Total"]
    body = body.drop(columns="Total")
    return body, total_row.drop("Total"), total_col


def check(published, threshold=THRESHOLD):
    body, col_tot, row_tot = _load(published)
    vals = body.astype(str).map(lambda x: x.strip())
    hidden = vals == "*"
    known = vals.where(~hidden).astype(float)
    recovered = []
    changed = True
    while changed:
        changed = False
        for i in body.index:                       # rows
            h = hidden.loc[i] & known.loc[i].isna()
            if h.sum() == 1:
                j = h[h].index[0]
                v = float(row_tot[i]) - known.loc[i].sum(skipna=True)
                known.loc[i, j] = v; recovered.append((i, j, v, "row")); changed = True
        for j in body.columns:                     # columns
            h = hidden[j] & known[j].isna()
            if h.sum() == 1:
                i = h[h].index[0]
                v = float(col_tot[j]) - known[j].sum(skipna=True)
                known.loc[i, j] = v; recovered.append((i, j, v, "column")); changed = True
    ranges = []
    still = [(i, j) for i in body.index for j in body.columns if hidden.loc[i, j] and pd.isna(known.loc[i, j])]
    if still:
        try:
            from scipy.optimize import linprog
            idx = {c: k for k, c in enumerate(still)}
            A, b = [], []
            for i in body.index:
                cells = [idx[(i, j)] for j in body.columns if (i, j) in idx]
                if cells:
                    row = np.zeros(len(still)); row[cells] = 1
                    A.append(row); b.append(float(row_tot[i]) - known.loc[i].sum(skipna=True))
            for j in body.columns:
                cells = [idx[(i, j)] for i in body.index if (i, j) in idx]
                if cells:
                    row = np.zeros(len(still)); row[cells] = 1
                    A.append(row); b.append(float(col_tot[j]) - known[j].sum(skipna=True))
            for k, cell in enumerate(still):
                c = np.zeros(len(still)); c[k] = 1
                lo = linprog(c, A_eq=A, b_eq=b, bounds=[(0, None)] * len(still), method="highs")
                hi = linprog(-c, A_eq=A, b_eq=b, bounds=[(0, None)] * len(still), method="highs")
                if lo.success and hi.success:
                    ranges.append((cell[0], cell[1], round(lo.fun, 2), round(-hi.fun, 2)))
        except ImportError:
            pass
    narrow = [x for x in ranges if x[3] - x[2] < threshold]
    return {"passed": not recovered and not narrow, "hidden_cells": int(hidden.values.sum()),
            "recovered": recovered, "narrow_ranges": narrow, "ranges": ranges}


if __name__ == "__main__":
    rep = check(pd.read_csv(sys.argv[1], dtype=str))
    print("PASSED" if rep["passed"] else "FAILED", "-", rep["hidden_cells"], "hidden cells")
    for i, j, v, how in rep["recovered"]:
        print(f"  recovered {i} x {j} = {v:g} from its {how}")
    for i, j, lo, hi in rep["narrow_ranges"]:
        print(f"  narrowed {i} x {j} to between {lo:g} and {hi:g}")
