# GasEntec LNG Demo 실행 순서

이 문서는 시연자가 사전에 구성한 Databricks 객체를 화면에서 보여주는 순서입니다.

## 1. Catalog·Schema·객체 관리

Catalog Explorer에서 다음을 먼저 보여줍니다.

```text
issu_dip_wksp
├─ gasentec_landing
│  └─ raw (Volume)
└─ gasentec_hands_on
   ├─ bronze_sites
   ├─ bronze_assets
   ├─ bronze_operations
   ├─ silver_sites
   ├─ silver_assets
   ├─ silver_operations_clean
   ├─ gold_lng_operations
   └─ lng_operations_metrics
```

```text
Landing Schema: 원천 파일과 Volume
Analytics Schema: 분석 테이블과 Metric View
Bronze: 원천 보존
Silver: 타입·범위·필수값 정제
Gold: 터미널·설비·운영 기록 결합
Metric View: AI/BI와 Genie가 사용하는 의미 계층
```

## 2. Lakeflow Declarative Pipeline

```text
Pipeline name: gasentec_lng_demo_pipeline
Source: notebooks/01_lng_demo_pipeline.sql
```

화면에서 Bronze → Silver → Gold DAG와 다음 품질 규칙을 보여줍니다.

```text
필수 ID NULL 제거
송출량·다운타임 음수 제거
uptime·BOG 비율 0~100 범위
유지보수 유형 표준화
ALARM·WATCH·NORMAL 상태 표준화
```

## 3. Lakeflow Job

```text
Job name: gasentec_lng_demo_refresh_job
```

Task 구성:

```text
Task name: run_medallion_pipeline
Task type: Pipeline
Pipeline: gasentec_lng_demo_pipeline
```

데모 환경에서는 Catalog·Schema·Volume을 Catalog Explorer에서 먼저 만들기 때문에 `setup_objects` Task를 추가하지 않습니다. Pipeline Task 하나만으로도 데이터 처리를 시연할 수 있습니다.

선택적으로 행 수 검증을 추가하려면 다음 Task를 `run_medallion_pipeline` 이후에 연결합니다.

```text
Task name: validate_pipeline
Task type: Notebook
Notebook path: notebooks/04_demo_validate.sql
Depends on: run_medallion_pipeline
```

## 4. Metric View

```text
SQL files:
notebooks/02_metric_view_baseline.sql
notebooks/03_metric_view_optimized.sql

Metric View:
issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
```

주요 측정값:

```text
total_sendout_mmscfd
average_uptime_pct
average_boiloff_rate_pct
total_downtime_hours
total_maintenance_cost_usd
incident_count
alarm_operation_count
corrective_maintenance_cost_usd
```

## 5. Genie Code로 AI/BI Dashboard 생성

AI/BI에서 `Create dashboard` 또는 Genie Code를 열고 다음 프롬프트를 사용합니다.

```text
`issu_dip_wksp.gasentec_hands_on.lng_operations_metrics` Metric View를 사용해 "GasEntec LNG Terminal Operations Overview"라는 이름의 AI/BI 대시보드를 만들어줘.

대상 사용자는 LNG 터미널 운영 및 O&M 검토 담당자야. 이 데이터는 실제 운영 데이터가 아닌 합성 데모 데이터라는 점을 대시보드 설명에 표시해줘.

다음 KPI 카드를 추가해줘.

1. 총 송출량: mmscfd 단위의 total_sendout_mmscfd 측정값
2. 평균 가동률: % 단위의 average_uptime_pct 측정값
3. 평균 BOG 비율: % 단위의 average_boiloff_rate_pct 측정값
4. 총 유지보수 비용: USD 단위의 total_maintenance_cost_usd 측정값

다음 시각화를 추가해줘.

1. operation_month별 총 송출량 월별 추이 선 그래프
2. site_name별 평균 가동률 내림차순 순위 막대 그래프
3. asset_category별 총 다운타임과 총 유지보수 비용 비교 그래프
4. site_name별 평균 BOG 비율과 평균 가동률 산점도
5. site_name과 asset_name별 ALARM 기록 수와 사고 건수 표

다음 필터를 대시보드 전체에 추가해줘.

- operation_month
- region
- terminal_type
- asset_category
- maintenance_type

원본 컬럼을 다시 집계하지 말고 Metric View에 정의된 측정값을 사용해줘. 차트 제목에 mmscfd, %, USD, 시간 단위를 표시해줘. 월별 차트는 operation_month를 시간순으로 정렬해줘.
```

## 6. Ask Genie

```text
전체 기간의 총 send-out은 얼마야?
터미널별 평균 가동률을 비교해줘
월별 send-out 추이를 보여줘
BOG 비율이 높은 상위 3개 설비를 보여줘
성능이 좋은 터미널을 알려줘
```

마지막 질문에는 send-out, uptime, BOG rate, downtime, maintenance cost 중 어떤 기준인지 되묻는지를 보여줍니다.

## 7. Genie Agent

```text
Space name: GasEntec LNG Operations Genie
Data source: issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
Instruction: resources/genie_instructions.md
Examples: resources/genie_example_queries.md
Benchmark: sample_data/support/genie_benchmarks.csv
```

Genie Agent는 운영 KPI·비교·추이·집계 질문을 담당하고, 정의·용어 질문은 Agent Bricks의 AI Search로 분리합니다.

## 8. Agent Bricks

### 8-1. Knowledge Assistant

검색 소스:

```text
output/pdf/gasentec_lng_domain_overview.pdf
output/pdf/gasentec_lng_om_playbook.pdf
```

테스트 질문:

```text
BOG가 무엇이고 왜 관리해야 하나요?
Regasification과 vaporizer의 관계를 설명해줘.
BOG rate가 올라가고 uptime이 내려가면 무엇을 확인해야 하나요?
```

### 8-2. AI Search 용어집

```text
Source table: issu_dip_wksp.gasentec_hands_on.gasentec_lng_glossary
Index: issu_dip_wksp.gasentec_hands_on.gasentec_lng_glossary_index
```

검색 질문:

```text
FSRU가 뭐야?
send-out의 의미를 알려줘.
Preventive maintenance와 Corrective maintenance의 차이는?
```

### 8-3. Supervisor

```text
Prompt: resources/supervisor_prompt.md

genie_agent       운영 수치·비교·추이·집계
ai_search         LNG 용어·약어·정의
dashboard_builder AI/BI Dashboard 생성·수정
clarification     기준·기간·대상이 모호한 질문
```

## 9. 간단한 Databricks Apps

```text
App name: gasentec-supervisor-demo
Resources: resources/app.yaml.example
Binding: resources/app_resource_binding.example.yml
Environment: GENIE_SPACE_ID, AI_SEARCH_INDEX, SUPERVISOR_AGENT_ENDPOINT
```

화면에는 질문 입력창, Supervisor route, 답변, 근거 문서 또는 Metric View, Genie Space·AI/BI Dashboard 링크를 배치합니다.

## 10. 데모 종료 시 확인

```text
Catalog Explorer 객체 계층
Pipeline DAG
Job task dependency
Metric View comment·synonym
AI/BI Dashboard
Ask Genie 응답
Genie Agent 응답
Knowledge Assistant 근거
AI Search 용어 검색
Supervisor route
Databricks App 화면
```
