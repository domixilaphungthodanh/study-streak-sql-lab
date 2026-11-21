WITH days AS (
 SELECT DISTINCT learner_id, studied_on FROM study_sessions
), numbered AS (
 SELECT *, ROW_NUMBER() OVER (PARTITION BY learner_id ORDER BY studied_on) AS day_number
 FROM days
), islands AS (
 SELECT *, date(studied_on, printf('-%d days',day_number)) AS group_day FROM numbered
)
SELECT learner_id, MIN(studied_on) AS start_day, MAX(studied_on) AS end_day, COUNT(*) AS days
FROM islands GROUP BY learner_id, group_day ORDER BY learner_id,start_day
