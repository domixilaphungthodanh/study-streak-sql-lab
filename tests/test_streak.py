import tempfile
from pathlib import Path
import unittest
from streak_lab.data import ROOT, connect, prepare
from streak_lab.analysis import checked, export

class StudyTests(unittest.TestCase):
    def test_sample(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            db = prepare(root/'sample.db', root/'raw')
            before = db.read_bytes()
            prepare(db, root/'raw')
            self.assertEqual(db.read_bytes(), before)
            other = prepare(root/'other.db', root/'raw')
            with connect(db) as c, connect(other) as d:
                self.assertEqual(list(c.iterdump()), list(d.iterdump()))
                tables = checked(c)
            self.assertEqual(tables['streaks'].query('learner_id == 1').days.tolist(), [3,2])
            self.assertEqual(tables['streaks'].query('learner_id == 2').days.tolist(), [2])
            summary = tables['summary'].set_index('learner_id')
            self.assertEqual(tuple(summary.loc[1,['sessions','study_days']]), (7,5))
            self.assertEqual(summary.loc[2,'best_weeks'], '2026-01-05, 2026-01-12')
            self.assertIsNone(summary.loc[20,'best_weeks'])
            self.assertEqual(summary.loc[20,'longest_streak'], 0)
            self.assertEqual(tables['weeks'].query('learner_id == 20').days.tolist(), [0]*8)
            self.assertEqual(len(tables['weeks']),160)

    def test_empty(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            db = root/'empty.db'
            with connect(db, readonly=False) as c:
                c.executescript((ROOT/'sql/schema.sql').read_text(encoding='utf-8'))
            self.assertTrue(all(t.empty for t in export(db,root/'out').values()))
            self.assertEqual(len(list((root/'out').glob('*.csv'))),3)
            self.assertTrue((root/'out/study_weeks.png').exists())
            self.assertTrue((root/'out/report.md').exists())
