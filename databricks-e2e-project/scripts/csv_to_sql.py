import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.joinpath('00_synthetic_data', 'data')
OUTPUT_SUFFIX = '_inserts.sql'

def fmt_value(v):
    if v is None:
        return 'NULL'
    s = v.strip()
    if s == '' or s.upper() == 'NULL':
        return 'NULL'
    # try int
    try:
        if '.' not in s:
            iv = int(s)
            return str(iv)
    except Exception:
        pass
    # try float
    try:
        fv = float(s)
        return str(fv)
    except Exception:
        pass
    # otherwise quote and escape single quotes
    s = s.replace("'", "''")
    return f"'{s}'"


def csv_to_sql(csv_path: Path):
    table = csv_path.stem
    out_path = csv_path.with_name(csv_path.stem + OUTPUT_SUFFIX)
    with csv_path.open(newline='', encoding='utf-8') as f, out_path.open('w', encoding='utf-8') as out:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return None
        cols = [h.strip() for h in headers]
        col_list = ', '.join([f'"{c}"' for c in cols])
        for row in reader:
            # pad shorter rows
            if len(row) < len(cols):
                row += [''] * (len(cols) - len(row))
            vals = ', '.join(fmt_value(v) for v in row[:len(cols)])
            out.write(f'INSERT INTO {table} ({col_list}) VALUES ({vals});\n')
    return out_path


def main():
    created = []
    for csv_file in sorted(DATA_DIR.glob('*.csv')):
        p = csv_to_sql(csv_file)
        if p:
            created.append(p)
    if created:
        print('Created SQL files:')
        for c in created:
            print(c)
    else:
        print('No CSV files processed.')

if __name__ == '__main__':
    main()
