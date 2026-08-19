# Databricks GasEntec LNG Demo

가스엔텍 소개용으로 미리 구축하는 Databricks 데모입니다. 참가자가 코드를 작성하는 실습이 아니라, Catalog·Schema·객체 관리부터 AI/BI·Agent Bricks·Databricks Apps까지 하나의 흐름으로 시연하는 구성을 목표로 합니다.

이 저장소의 프로젝트명, 설비명, 운영 수치, 비용은 모두 합성 데이터입니다. 공개된 LNG 솔루션 범주를 학습 도메인으로만 참고하며 실제 고객·프로젝트·운영 데이터를 포함하지 않습니다.

## 시연 흐름

```text
Catalog / Schema / Volume / Table
        ↓
Lakeflow Declarative Pipeline
        ↓
Lakeflow Job
        ↓
Metric View
        ↓
Genie Code로 AI/BI Dashboard 생성 + Ask Genie
        ↓
Genie Agent
        ↓
Agent Bricks
  ├─ Knowledge Assistant (PDF)
  ├─ AI Search (LNG 용어집)
  └─ Supervisor
        ↓
Databricks Apps
```

## 대상 Workspace

```text
Profile: issu-dip-wksp (Default)
Host: https://dbc-9f87ed8e-e4c2.cloud.databricks.com
SQL Warehouse: Serverless Starter Warehouse
Warehouse ID: 3090f2a1f1105378
```

## Unity Catalog 객체

```text
Catalog: issu_dip_wksp
Landing Schema: gasentec_landing
Analytics Schema: gasentec_hands_on
Volume: gasentec_landing.raw
Gold table: gasentec_hands_on.gold_lng_operations
Metric View: gasentec_hands_on.lng_operations_metrics
```

## 시연용 데이터

```text
sample_data/raw/sites.csv                         터미널/프로젝트 차원 4행
sample_data/raw/assets.csv                        LNG 설비 차원 12행
sample_data/raw/operations/operations_batch_*.csv 운영·O&M 사실 데이터 300행
sample_data/support/glossary.csv                  LNG 용어집 8행
```

## 시연 순서

1. [`docs/00_demo_environment.md`](docs/00_demo_environment.md)에서 기존 Catalog `issu_dip_wksp` 아래에 Schema·Volume을 화면으로 만들고 CSV를 Volume에 업로드합니다.
2. `notebooks/00_demo_environment.sql`은 필요할 때 객체와 업로드 상태를 SQL로 확인하는 참고 파일입니다.
3. `notebooks/01_lng_demo_pipeline.sql`을 Lakeflow Declarative Pipeline으로 등록·실행합니다.
4. `resources/gasentec_demo.resources.yml`의 Lakeflow Job으로 Pipeline과 SQL 검증 흐름을 확인합니다.
5. `notebooks/02_metric_view_baseline.sql` 및 `03_metric_view_optimized.sql`로 Metric View를 생성합니다.
6. `resources/ai_bi_dashboard_prompts.md`의 Genie Code 프롬프트로 AI/BI Dashboard를 만들고 [`resources/ask_genie_demo_script.md`](resources/ask_genie_demo_script.md)의 Ask Genie 질문을 시연합니다.
7. `resources/genie_instructions.md`와 `resources/genie_example_queries.md`로 Genie Agent를 구성합니다.
8. [`resources/agent_bricks_demo_plan.md`](resources/agent_bricks_demo_plan.md)에 따라 Knowledge Assistant, AI Search 용어집, Supervisor를 구성합니다.
9. `resources/app.yaml.example`과 `resources/app_resource_binding.example.yml`을 기준으로 간단한 Databricks App을 연결합니다.

App 소스 예제는 `app/app.py`, `app/app.yaml`, `app/requirements.txt`에 있습니다. Streamlit 화면에서 Supervisor endpoint에 질문을 보내고, Supervisor가 Genie Agent·Knowledge Assistant·AI Search를 선택해 답변하도록 구성합니다.

## Knowledge Assistant PDF

```text
output/pdf/gasentec_lng_domain_overview.pdf
output/pdf/gasentec_lng_om_playbook.pdf
output/pdf/knowledge_assistant_test_questions.pdf
output/pdf/assets/lng_terminal_illustration.png
```

첫 번째와 두 번째 PDF를 검색 소스로 연결하고, 세 번째 PDF는 테스트 질문 목록으로 별도 사용합니다.

## 문서

- [데이터 상세 가이드](docs/02_data_guide.md)
- [Demo 환경 구성](docs/00_demo_environment.md)
- [Demo 실행 순서](docs/01_demo_runbook.md)
- [Demo 설계](DEMO_DESIGN.md)
- [Agent Bricks 구성 계획](resources/agent_bricks_demo_plan.md)
- [GitHub 게시](docs/00_github_publish.md)

CSV는 Excel에서 한글이 깨지지 않도록 UTF-8-SIG로 생성합니다.
