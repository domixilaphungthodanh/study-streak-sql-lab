from collections import Counter
from datetime import date, timedelta
import pandas as pd

from .data import DB, FIRST, ROOT, connect, validate

STREAK_COLUMNS = ["learner_id", "start_day", "end_day", "days"]
WEEK_COLUMNS = ["learner_id", "week", "days"]
SUMMARY_COLUMNS = ["learner_id", "name", "sessions", "study_days", "longest_streak", "best_days", "best_weeks"]


def read_sql(name):
    return (ROOT / f"sql/{name}.sql").read_text(encoding="utf-8")


def pandas_tables(connection):
    learners = pd.read_sql_query("SELECT * FROM learners ORDER BY learner_id", connection)
    sessions = pd.read_sql_query("SELECT * FROM study_sessions", connection)
    grouped = dict(tuple(sessions.groupby("learner_id")))
    streaks, weeks, summary = [], [], []
    for learner in learners.itertuples(index=False):
        group = grouped.get(learner.learner_id, sessions.iloc[:0])
        dates = sorted({date.fromisoformat(day) for day in group.studied_on})
        runs = []
        for day in dates:
            if runs and (day - runs[-1][-1]).days == 1:
                runs[-1].append(day)
            else:
                runs.append([day])
        for run in runs:
            streaks.append((learner.learner_id, run[0].isoformat(), run[-1].isoformat(), len(run)))
        counts = Counter((day - FIRST).days // 7 for day in dates)
        best = max(counts.values(), default=0)
        tied = []
        for index in range(8):
            week = (FIRST + timedelta(weeks=index)).isoformat()
            weeks.append((learner.learner_id, week, counts[index]))
            if best and counts[index] == best:
                tied.append(week)
        summary.append((learner.learner_id, learner.name, len(group), len(dates),
                        max(map(len, runs), default=0), best, ", ".join(tied) or None))
    return dict(streaks=pd.DataFrame(streaks, columns=STREAK_COLUMNS),
                weeks=pd.DataFrame(weeks, columns=WEEK_COLUMNS),
                summary=pd.DataFrame(summary, columns=SUMMARY_COLUMNS))


def checked(connection):
    validate(connection)
    streaks, weeks = read_sql("streaks"), read_sql("weeks")
    queries = dict(streaks=streaks, weeks=weeks, summary=read_sql("summary").format(streaks=streaks, weeks=weeks))
    actual = {name: pd.read_sql_query(sql, connection) for name, sql in queries.items()}
    expected = pandas_tables(connection)
    for name in actual:
        pd.testing.assert_frame_equal(actual[name], expected[name], check_dtype=False, check_exact=True)
    return actual


def export(db=DB, output=ROOT / "outputs"):
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    with connect(db) as connection:
        tables = checked(connection)
    output.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output/f"{name}.csv", index=False, encoding="utf-8-sig")
    focus = tables["weeks"][tables["weeks"].learner_id.eq(1)]
    fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
    if focus.empty:
        ax.text(.5, .5, "Chưa có người học mẫu", ha="center", transform=ax.transAxes)
    else:
        ax.bar(focus.week.str[5:], focus.days, color="#226876")
    ax.set(title="Ngày học theo tuần của người học 01", xlabel="Ngày thứ Hai (tháng-ngày)",
           ylabel="Số ngày", ylim=(0, 7), yticks=range(8))
    fig.savefig(output/"study_weeks.png", dpi=140)
    plt.close(fig)
    summary = tables["summary"]
    example = summary[summary.learner_id.eq(1)]
    detail = (f"Người học 01 có {example.sessions.iloc[0]} buổi trong {example.study_days.iloc[0]} ngày."
              if len(example) else "Dữ liệu rỗng, có 0 người học mẫu.")
    (output/"report.md").write_text(
        "# Chuỗi ngày học giả lập\n\nKỳ 05/01–01/03/2026, tuần thứ Hai–Chủ nhật.\n\n"
        f"1. {detail}\n"
        f"2. Có {len(tables['streaks'])} chuỗi trong {len(summary)} người học.\n"
        f"3. Chuỗi dài nhất toàn bộ dữ liệu là {max(summary.longest_streak, default=0)} ngày.\n",
        encoding="utf-8")
    return tables

