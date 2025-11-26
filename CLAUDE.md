# CLAUDE.md - Development Guidelines

## Project Overview

Kafka Python consumer/producer application with Kubernetes deployment support.

## Tech Stack

- **Language**: Python 3.12+
- **Kafka Client**: kafka-python-ng 2.2.2
- **Container Runtime**: Kubernetes (StatefulSet)
- **Deployment Pattern**: ConfigMap + Init Container (no custom image build)

## Project Structure

```
kafka-py/
├── consumer.py          # Kafka consumer implementation
├── producer.py          # Kafka producer implementation
├── requirements.txt     # Python dependencies
└── k8s/                 # Kubernetes manifests
    ├── namespace.yaml
    ├── configmap-config.yaml    # Environment configuration
    ├── configmap-scripts.yaml   # Python scripts as ConfigMap
    ├── consumer-statefulset.yaml
    └── producer-statefulset.yaml
```

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Coding Conventions

### Documentation

- Documents are written in English by default
- Korean is used selectively where clarity is needed (e.g., user-facing instructions, Korean-specific guidelines)
- Code comments in English

### Python

- Use docstrings for functions
- Use `argparse` for CLI arguments
- JSON serialization for Kafka messages
- Graceful shutdown handling with try/finally
- Use `socket.gethostname()` for client identification

### Kubernetes

- All resources in `kafka-apps` namespace
- StatefulSet for ordered pod naming
- ConfigMap for configuration and scripts
- Init container pattern for dependency installation

## Git Workflow (REQUIRED)

### Commit Rules

1. **Commit after every meaningful change** - Do not batch unrelated changes
2. **Commit message in Korean** - 커밋 메시지는 한국어로 작성
3. **Commit message format** - `<대상> <동작>` 형식 사용
   ```
   # 동작 유형
   X 추가          # 새 기능/파일 추가
   X 수정          # 버그 수정
   X 업데이트      # 기존 기능 개선
   X 리팩토링      # 코드 구조 개선
   X 제거          # 기능/파일 삭제

   # 예시
   Kafka consumer 추가
   K8s 매니페스트 업데이트
   client_id 지원 추가 및 StatefulSet 리팩토링
   CLAUDE.md 가이드라인 업데이트
   ```
4. **Always verify before commit**:
   ```bash
   git status
   git diff
   ```

### Push Rules

1. **Push immediately after commit** - Every commit must be pushed
2. **Push command**:
   ```bash
   git push -u origin <branch-name>
   ```
3. **On push failure**: Retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s)

### Workflow Steps

```bash
# 1. Check current status
git status

# 2. Stage changes
git add <files>

# 3. Commit with clear message
git commit -m "Add/Fix/Update: description"

# 4. Push immediately
git push -u origin <branch-name>

# 5. Verify push succeeded
git status
```

## Testing & Validation

### Local Testing

```bash
# Test consumer
python consumer.py --bootstrap-servers localhost:9092 --topic test-topic

# Test producer
python producer.py --bootstrap-servers localhost:9092 --topic test-topic --num-messages 5
```

### Kubernetes Deployment

```bash
# Deploy
kubectl apply -f k8s/

# Verify pods
kubectl get pods -n kafka-apps

# Check logs
kubectl logs -f statefulset/kafka-consumer -n kafka-apps
kubectl logs -f statefulset/kafka-producer -n kafka-apps

# Update after code changes
kubectl apply -f k8s/configmap-scripts.yaml
kubectl rollout restart statefulset/kafka-consumer statefulset/kafka-producer -n kafka-apps
```

### Post-Test Documentation Update (REQUIRED)

테스트 완료 후 반드시 관련 문서를 최신화:

1. **README.md** - 사용법, 설정값 변경 시 갱신
2. **CLAUDE.md** - 개발 가이드라인 변경 시 갱신
3. **k8s/configmap-config.yaml** - 환경변수 추가/변경 시 Configuration Reference 테이블 갱신
4. **requirements.txt** - 의존성 변경 시 Tech Stack 섹션 갱신

## Configuration Reference

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker addresses |
| `KAFKA_TOPIC` | `test-topic` | Target topic |
| `KAFKA_GROUP_ID` | `my-consumer-group` | Consumer group |
| `KAFKA_OFFSET_RESET` | `earliest` | Offset reset strategy |
| `KAFKA_NUM_MESSAGES` | `10` | Messages to send (producer) |
| `KAFKA_DELAY` | `1.0` | Delay between messages (producer) |

## Important Notes

- Consumer uses hostname as `client_id` for broker identification
- Producer has retry logic (5 retries, 500ms backoff)
- K8s deployment uses `python:3.12-slim` base image
- Scripts are mounted read-only from ConfigMap
