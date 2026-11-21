CREATE TABLE learners(learner_id INTEGER PRIMARY KEY,name TEXT NOT NULL) STRICT;
CREATE TABLE study_sessions(
 session_id INTEGER PRIMARY KEY,learner_id INTEGER NOT NULL REFERENCES learners,
 studied_on TEXT NOT NULL CHECK(studied_on BETWEEN '2026-01-05' AND '2026-03-01'
 AND date(studied_on) IS studied_on),
 minutes INTEGER NOT NULL CHECK(minutes>0)
) STRICT;
CREATE INDEX study_days ON study_sessions(learner_id,studied_on);
