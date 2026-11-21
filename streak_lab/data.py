from contextlib import closing
from datetime import date, timedelta
from pathlib import Path
import csv
import os
import random
import sqlite3
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database/streak.db"
FIRST = date(2026, 1, 5)
TABLES = ("learners", "study_sessions")


def connect(path=DB, *, readonly=True):
    path = Path(path).resolve()
    database = path.as_uri() + "?mode=ro" if readonly else path
    connection = sqlite3.connect(database, uri=readonly)
    connection.execute("PRAGMA foreign_keys=ON")
    return closing(connection)


def populate(connection):
    randomizer = random.Random(42)
    connection.executescript((ROOT / "sql/schema.sql").read_text(encoding="utf-8"))
    connection.executemany("INSERT INTO learners VALUES (?,?)",
                           [(i, f"Người học {i:02}") for i in range(1, 21)])
    rows = [(1, f"2026-01-{day:02}", 30) for day in (5, 6, 6, 6, 7, 9, 10)]
    rows.extend((2, f"2026-01-{day:02}", 25) for day in (11, 12))
    for learner in range(3, 20):
        for offset in range(56):
            if randomizer.random() < 0.55:
                rows.append((learner, (FIRST + timedelta(days=offset)).isoformat(),
                             randomizer.randint(15, 90)))
    connection.executemany(
        "INSERT INTO study_sessions(learner_id,studied_on,minutes) VALUES (?,?,?)", rows)


def prepare(db=DB, output=ROOT / "data/raw"):
    if not db.exists():
        db.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=db.parent) as folder:
            temporary = Path(folder) / "sample.db"
            with connect(temporary, readonly=False) as connection, connection:
                populate(connection)
                validate(connection)
            try:
                os.link(temporary, db)
            except FileExistsError:
                pass
    with connect(db) as connection:
        validate(connection)
        output.mkdir(parents=True, exist_ok=True)
        for table in TABLES:
            rows = connection.execute(f"SELECT * FROM {table} ORDER BY 1")
            with (output / f"{table}.csv").open("w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow([column[0] for column in rows.description])
                writer.writerows(rows)
    return db


def validate(connection):
    if connection.execute("PRAGMA foreign_key_check").fetchone():
        raise ValueError("Khóa ngoại không hợp lệ")
    if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise ValueError("SQLite bị lỗi")

