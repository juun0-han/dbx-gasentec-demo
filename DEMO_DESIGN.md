# GasEntec LNG Databricks Demo 설계

## 데모 목적

코드 작성 실습이 아니라, 하나의 LNG 운영 데이터셋을 바탕으로 Databricks의 데이터·AI 기능이 연결되는 모습을 보여줍니다.

```text
Catalog / Schema / Volume / Tables
  → Lakeflow Declarative Pipeline
  → Lakeflow Job
  → Metric View
  → Genie Code Dashboard + Ask Genie
  → Genie Agent
  → Agent Bricks: Knowledge Assistant + AI Search + Supervisor
  → Databricks Apps
```

## 대상 환경

```text
Workspace profile: issu-dip-wksp (Default)
Workspace URL: https://dbc-9f87ed8e-e4c2.cloud.databricks.com
Warehouse: Serverless Starter Warehouse
Warehouse ID: 3090f2a1f1105378
```

## 객체 구조

| 계층 | 객체 | 용도 |
|---|---|---|
| Catalog | `issu_dip_wksp` | Workspace에서 제공하는 기존 Unity Catalog |
| Landing Schema | `gasentec_landing` | Volume·원천 데이터 |
| Analytics Schema | `gasentec_hands_on` | Bronze·Silver·Gold·Metric View |
| Volume | `gasentec_landing.raw` | CSV 및 용어집 적재 |
| Gold | `gold_lng_operations` | 터미널·설비·운영 기록 통합 |
| Metric View | `lng_operations_metrics` | Genie·Dashboard 공통 의미 계층 |

## 시연 모듈

### 1. Catalog·Schema·객체 관리

Catalog, Landing/Analytics Schema, Volume을 먼저 만들고, Catalog Explorer에서 테이블·컬럼·코멘트·품질 계층을 보여줍니다.

### 2. LDP와 Lakeflow Job

`bronze_sites`, `bronze_assets`, `bronze_operations`에서 `silver_*`를 거쳐 `gold_lng_operations`가 만들어지는 DAG를 보여줍니다. Lakeflow Job은 객체 준비, Pipeline 실행, SQL 검증 task를 순서대로 연결합니다.

### 3. Metric View

송출량, 가동률, BOG 비율, 다운타임, 유지보수 비용, 사고·알람 수를 하나의 표준 의미 계층으로 제공합니다. 컬럼 설명·동의어·단위·다의어 규칙을 함께 보여줍니다.

### 4. Genie Code Dashboard와 Ask Genie

Genie Code 프롬프트로 KPI 카드, 월별 추이, 터미널 비교, 설비 카테고리 비용, BOG-가동률 관계를 생성합니다. 같은 Metric View에서 Ask Genie 질문을 실행해 Dashboard와 대화형 분석이 동일한 기준을 사용하는지 보여줍니다.

### 5. Genie Agent

운영 KPI·비교·추이 질문을 Metric View에 연결하고, Example Query와 Instruction으로 응답 형식을 안정화합니다.

### 6. Agent Bricks

- Knowledge Assistant: LNG 도메인 PDF 기반 정의·요약·근거 검색
- AI Search: `glossary.csv` 기반 LNG 용어·약어·동의어 검색
- Supervisor: Genie Agent, Knowledge Assistant, AI Search, Dashboard Builder, Clarification 라우팅

### 7. Databricks Apps

간단한 질문 입력 화면에서 Supervisor route, 답변, 근거 문서, Genie Space 또는 AI/BI Dashboard 링크를 보여줍니다.

## 데이터 범위

| 구분 | 파일 | 규모 |
|---|---|---:|
| 터미널 차원 | `sites.csv` | 4행 |
| 설비 차원 | `assets.csv` | 12행 |
| 운영 사실 | `operations_batch_001~003.csv` | 300행 |
| 용어집 | `glossary.csv` | 8행 |
| 평가 질문 | Genie·Agent CSV/PDF | 소량 |

모든 프로젝트명·수치·비용은 합성 데이터입니다.

## 데모 완료 기준

- 대상 Workspace에 Catalog·Schema·Volume·테이블이 생성됨
- Pipeline DAG와 Lakeflow Job task dependency가 표시됨
- Metric View의 측정값과 설명이 Catalog Explorer에 표시됨
- Genie Code로 AI/BI Dashboard가 생성됨
- Ask Genie와 Genie Agent가 동일 Metric View를 사용함
- Agent Bricks의 Knowledge Assistant·AI Search·Supervisor가 질문에 맞게 라우팅됨
- Databricks App에서 질문·route·답변·근거 링크가 한 화면에 표시됨
