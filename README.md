# FastAPI Server

## 1. 설치 및 실행

```shell
# 실행(로컬)
sh init.sh

# Swagger UI url: /docs
```

## 2. 전체 Test 진행

```shell
# 실행(로컬)
sh test.sh

# Swagger UI url: /docs
```

## 3. Service 등록하기

### service file 생성

```
# sudo nano /etc/systemd/system/fastapi.service
[Unit]
Description=Run FastAPI uvicorn server

[Service]
Type=simple
WorkingDirectory=/home/ec2-user/service/PROJECT_NAME
ExecStart=/bin/bash /home/ec2-user/service/PROJECT_NAME/init.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Service 등록하기

```
sudo systemctl start fastapi.service
```

### Service 등록 확인하기

```
sudo systemctl status fastapi.service
```

```shell
# result
[ec2-user@ip-172-31-46-155 AuditLog-backend-V2]$ sudo systemctl status audilog.service
● audilog.service - Run AuditLog FastAPI uvicorn server
   Loaded: loaded (/etc/systemd/system/audilog.service; disabled; vendor preset: disabled)
   Active: active (running) since 화 1970-01-01 00:00:00 UTC; 2s ago
 Main PID: 3475 (bash)
   CGroup: /system.slice/audilog.service
           ├─3475 /bin/bash /home/ec2-user/service/AuditLog-backend-V2/init.sh
           ├─3481 python3 bin/run.py
           ├─3482 /home/ec2-user/service/AuditLog-backend-V2/venv/bin/python3 -c from multiprocessing.semaphore_tracker import main;main(4)
           └─3483 /home/ec2-user/service/AuditLog-backend-V2/venv/bin/python3 -c from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=5, pipe_handle=7) --multipr...

01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: Requirement already satisfied: charset-normalizer~=2.0.0; python_version >= "3" in ./venv/...(2.0.9)
01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: Requirement already satisfied: pycparser in ./venv/lib/python3.7/site-packages (from cffi>... (2.21)
01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: Requirement already satisfied: zipp>=0.5 in ./venv/lib/python3.7/site-packages (from impor...(3.6.0)
01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: WARNING: You are using pip version 20.1.1; however, version 21.3.1 is available.
01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: You should consider upgrading via the '/home/ec2-user/service/AuditLog-backend-V2/venv/bin...ommand.
01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: INFO:     Started reloader process [3481] using statreload
01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: INFO:     Started server process [3483]
01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: INFO:     Waiting for application startup.
01월 01 00:00:00 ip-0-0-0-0.ap-northeast-2.compute.internal bash[3475]: INFO:     Application startup complete.

```

-----

