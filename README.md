# Tên models 
# Cấu trúc thư mục
```
template-api
├── config
├──── config.py # Đây là file chính để cấu hình những config cho server
├── docker
├──── Dockerfile # File này dành cho những model dùng GPU
├──── Dockerfile-cpu # CPU
├── handler
├──── client_exceptions.py # Những mã code trả về từ client
├──── server_exceptions.py # Những mã code trả về từ phía server
├── logs
├──── logs.py # Cấu hình logs cho ELK
├── models
├──── models.py # File này là inference export model AI 
├── prometheus
├──── metrics # Cấu hình những metrics để cho gafana
├── trace
├──── trace.py # Cấu hình việc quá trình call của api như thế nào
├── utils 
├──── index.py # Chứa những hàm dùng chung
├── weights # folder chứa trọng số
├── .env # File môi trường
├── app.py # App chính để run ứng dụng
├── requirements.txt # File tải những cấu hình cần thiết
├── .gitignore

```
# Mục đích
# Môi trường
# Hướng dẫn sử dụng
