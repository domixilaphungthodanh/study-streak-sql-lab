# Study Streak SQL Lab

Dữ liệu giả lập gồm 20 người học trong 8 tuần từ 05/01 đến 01/03/2026. Bài học kéo dài 1–2 ngày. Dùng Python 3.12, SQLite, pandas, Matplotlib và Jupyter.

## Chạy trên Windows

Giải nén ZIP rồi mở thư mục có `run_streak.py` trong File Explorer. Gõ `powershell` vào thanh địa chỉ và nhấn Enter. Lần đầu cần mạng để cài thư viện.

```powershell
Get-Location
Get-ChildItem
python prepare.py
python analyze.py
python run_streak.py --notebook
```

Nếu thiếu launcher, dùng `cd "đường dẫn thư mục dự án"`. Prepare tạo SQLite và CSV nguồn trong data/raw, chạy lại dùng database đã có. Analyze tạo ba CSV, một PNG và báo cáo trong outputs. Hai file START_WINDOWS.cmd và START_NOTEBOOK.cmd chạy bằng nhấp đúp.

Nhập lệnh khởi động trong PowerShell. Trong Jupyter, dùng Shift+Enter từng ô Python chứa truy vấn SQL. Nếu thấy tab Running, chọn Files rồi mở notebooks/02_analysis.ipynb.

## Lịch học

Ngày 1 đọc từ điển rồi chạy phần DISTINCT và ROW_NUMBER. Người 01 có 7 buổi trong 5 ngày, tạo hai chuỗi 3 và 2 ngày. Ngày 2 đọc tuần đồng hạng, biểu đồ và làm 10 bài tập. Notebook mở SQLite chỉ đọc.

[Từ điển dữ liệu](docs/data_dictionary.md) · [Bài tập](docs/exercises.md) · [Lời giải](docs/solutions.md)

Mã MIT. Dùng `git log --oneline` để xem năm bước và `git show` kèm mã commit để đọc từng bước.
