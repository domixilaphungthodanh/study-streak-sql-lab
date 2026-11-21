# Lời giải

## 1. Đếm người học

```sql
SELECT COUNT(*) FROM learners
```

## 2. Đếm buổi của người 01

```sql
SELECT COUNT(*) FROM study_sessions WHERE learner_id=1
```

## 3. Đếm ngày của người 01

```sql
SELECT COUNT(DISTINCT studied_on) FROM study_sessions WHERE learner_id=1
```

## 4. Tìm ngày có nhiều buổi

```sql
SELECT learner_id,studied_on,COUNT(*) FROM study_sessions GROUP BY learner_id,studied_on HAVING COUNT(*)>1
```

## 5. Tính phút học theo người

```sql
SELECT learner_id,SUM(minutes) FROM study_sessions GROUP BY learner_id
```

## 6. Tìm người chưa học

```sql
SELECT * FROM learners l WHERE NOT EXISTS (SELECT 1 FROM study_sessions s WHERE s.learner_id=l.learner_id)
```

## 7. Đánh số ngày học

```sql
SELECT *,ROW_NUMBER() OVER(PARTITION BY learner_id ORDER BY studied_on) FROM (SELECT DISTINCT learner_id,studied_on FROM study_sessions)
```

## 8. Xem hai chuỗi của người 01

Bọc truy vấn streaks.sql trong SELECT và lọc learner_id=1.

## 9. Tìm tuần không học

Bọc truy vấn weeks.sql trong SELECT và lọc days=0.

## 10. Tìm người đồng hạng nhiều tuần

Đọc summary.csv và tìm best_weeks chứa dấu phẩy.
