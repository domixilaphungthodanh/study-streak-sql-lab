WITH streaks AS ({streaks}), weeks AS ({weeks}), best AS (
 SELECT learner_id,MAX(days) AS best_days FROM weeks GROUP BY learner_id
), longest AS (
 SELECT learner_id,MAX(days) AS longest_streak FROM streaks GROUP BY learner_id
), activity AS (
 SELECT learner_id,COUNT(*) AS sessions,COUNT(DISTINCT studied_on) AS study_days
 FROM study_sessions GROUP BY learner_id
), tied AS (
 SELECT w.learner_id,group_concat(w.week,', ') AS best_weeks
 FROM (SELECT * FROM weeks ORDER BY learner_id,week) w JOIN best b USING(learner_id)
 WHERE w.days=b.best_days AND w.days>0 GROUP BY w.learner_id
)
SELECT l.learner_id,l.name,COALESCE(sessions,0) AS sessions,COALESCE(study_days,0) AS study_days,
 COALESCE(longest_streak,0) AS longest_streak,best_days,best_weeks
FROM learners l JOIN best USING(learner_id)
LEFT JOIN tied USING(learner_id)
LEFT JOIN longest USING(learner_id)
LEFT JOIN activity USING(learner_id)
ORDER BY l.learner_id

