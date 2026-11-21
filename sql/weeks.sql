WITH RECURSIVE calendar(week) AS (
 VALUES ('2026-01-05')
 UNION ALL SELECT date(week,'+7 days') FROM calendar WHERE week<'2026-02-23'
), daily AS (
 SELECT DISTINCT learner_id,studied_on FROM study_sessions
)
SELECT l.learner_id,week,COUNT(d.studied_on) AS days
FROM learners l CROSS JOIN calendar
LEFT JOIN daily d ON d.learner_id=l.learner_id AND studied_on>=week AND studied_on<date(week,'+7 days')
GROUP BY l.learner_id,week ORDER BY l.learner_id,week
