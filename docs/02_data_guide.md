# GasEntec LNG 데모 데이터 가이드

이 문서는 GasEntec LNG 데모에서 사용하는 데이터의 의미와 구조를 설명합니다. Databricks 기능을 실행하기 전에 이 문서를 읽으면 각 테이블과 컬럼이 어떤 업무를 표현하는지 이해할 수 있습니다.

이 데이터는 실제 회사의 운영 데이터가 아닌, LNG 터미널 운영·설비·유지보수 업무를 시연하기 위해 만든 합성 데이터입니다. 터미널명, 수치, 국가, 운영 기록은 데모 목적의 예시입니다.

## 1. 데모에서 표현하는 업무

이 데모는 LNG 터미널과 설비의 운영 현황을 분석하는 상황을 가정합니다.

```text
LNG 터미널
  └─ 여러 설비
       └─ 시간대별 운영 기록
            ├─ 송출량
            ├─ 처리량
            ├─ 가동률
            ├─ BOG 비율
            ├─ 중단 시간
            ├─ 유지보수 비용
            └─ 사고·알람 상태
```

데이터 관계는 다음과 같습니다.

```text
sites.csv
  1개 터미널
      └── 여러 설비
            assets.csv
                └── 여러 운영 기록
                      operations_batch_*.csv
```

예를 들어 `S001` 터미널에는 여러 설비가 있고, 각 설비에는 여러 날짜의 운영 기록이 연결됩니다.

## 2. 파일과 데이터 건수

### 2.1 원천 데이터

원천 데이터는 `sample_data/raw` 폴더에 있습니다.

| 파일 | 설명 | 예상 건수 | 데이터 성격 |
|---|---|---:|---|
| `sites.csv` | LNG 터미널·프로젝트 마스터 | 4 | 기준 정보 |
| `assets.csv` | 터미널별 설비 마스터 | 12 | 기준 정보 |
| `operations/operations_batch_001.csv` | 운영 기록 1차 배치 | 100 | 실적 데이터 |
| `operations/operations_batch_002.csv` | 운영 기록 2차 배치 | 100 | 실적 데이터 |
| `operations/operations_batch_003.csv` | 운영 기록 3차 배치 | 100 | 실적 데이터 |

운영 기록은 총 300건입니다. 세 개의 배치 파일로 나눈 이유는 Lakeflow Declarative Pipelines의 증분 파일 처리와 Auto Loader 흐름을 보여주기 위해서입니다.

### 2.2 지원 데이터

지원 데이터는 `sample_data/support` 폴더에 있습니다. 이 파일들은 운영 파이프라인의 원천 입력이 아니라, 데이터 검증·Genie·AI Search·Supervisor 데모에 사용합니다.

| 파일 | 사용 목적 |
|---|---|
| `data_dictionary.csv` | 컬럼명, 데이터 타입, 업무 정의 확인 |
| `expected_results.csv` | 파이프라인 결과 건수와 기본 검증 |
| `genie_benchmarks.csv` | Genie 질문별 기대 측정값과 결과 형태 정의 |
| `genie_example_queries.csv` | Genie 예제 질문, 예상 SQL, 설명 포인트 |
| `glossary.csv` | AI Search에서 사용할 LNG 용어집 |
| `agent_evaluation.csv` | Supervisor Agent의 라우팅과 응답 방식 평가 |

## 3. `sites.csv`: 터미널 마스터

`sites.csv`는 LNG 터미널 또는 프로젝트의 기본 정보를 관리합니다. 카페 데이터에서 매장 마스터에 해당하는 데이터입니다.

| 컬럼 | 의미 | 예시 |
|---|---|---|
| `site_id` | 터미널 식별자 | `S001` |
| `site_name` | 터미널명 | `Philippines Hybrid Terminal (Demo)` |
| `country` | 국가 | `Philippines` |
| `region` | 권역 | `Asia` |
| `terminal_type` | 터미널 유형 | `HYBRID`, `FLOATING`, `ONSHORE` |
| `commissioned_date` | 운영 시작일 | `2021-06-01` |
| `design_sendout_mmscfd` | 설계 기준 송출능력 | `500` |
| `site_status` | 터미널 운영 상태 | `ACTIVE` |

`site_id`는 터미널을 구분하는 기본 키입니다. `assets.csv`와 운영 기록에서 이 값을 사용해 어느 터미널의 데이터인지 연결합니다.

## 4. `assets.csv`: 설비 마스터

`assets.csv`는 각 터미널에 설치된 설비 정보를 관리합니다. 운영 기록만 보면 설비의 이름이나 중요도를 알 수 없기 때문에 별도의 마스터로 분리했습니다.

| 컬럼 | 의미 | 예시 |
|---|---|---|
| `asset_id` | 설비 식별자 | `A001` |
| `site_id` | 설비가 소속된 터미널 | `S001` |
| `asset_name` | 설비명 | `RegasTainer Module 01` |
| `asset_category` | 설비 분류 | `REGASIFICATION` |
| `criticality` | 설비 중요도 | `HIGH`, `MEDIUM`, `LOW` |

주요 설비 분류는 다음과 같습니다.

| 값 | 의미 |
|---|---|
| `REGASIFICATION` | LNG를 기화해 천연가스로 전환하는 설비 |
| `BOG_MANAGEMENT` | 증발가스(BOG)를 관리하는 설비 |
| `CARGO_HANDLING` | LNG 선박 또는 차량 하역 설비 |
| `COLD_TECH` | 저온 상태를 유지·관리하는 설비 |
| `PRESSURE_MANAGEMENT` | 압력 제어 설비 |
| `RELIQUEFACTION` | 기화된 가스를 다시 액화하는 설비 |

`criticality`는 설비 장애가 전체 운영에 미치는 영향을 나타냅니다. `HIGH` 설비는 장애가 발생했을 때 우선적으로 확인해야 하는 설비라는 의미입니다.

## 5. `operations_batch_*.csv`: 운영 실적

운영 기록은 분석의 중심이 되는 사실 데이터입니다. 하나의 행은 특정 시각에 특정 설비에서 발생한 하나의 운영 기록을 의미합니다.

| 컬럼 | 의미 | 단위 또는 값 |
|---|---|---|
| `operation_id` | 운영 기록 식별자 | `OP00001` |
| `operation_ts` | 운영 기록 발생 시각 | 타임스탬프 |
| `site_id` | 터미널 식별자 | `S001` |
| `asset_id` | 설비 식별자 | `A001` |
| `shift` | 교대 구분 | `DAY`, `NIGHT` |
| `sendout_mmscfd` | 천연가스 송출량 | mmscfd |
| `throughput_mmbtu` | 처리한 에너지량 | MMBtu |
| `boiloff_rate_pct` | BOG 비율 | % |
| `uptime_pct` | 설비 가동률 | % |
| `downtime_hours` | 설비 중단 시간 | 시간 |
| `maintenance_type` | 유지보수 유형 | `NONE`, `PREVENTIVE`, `CORRECTIVE`, `INSPECTION` |
| `maintenance_cost_usd` | 유지보수 비용 | USD |
| `incident_count` | 사고 건수 | 정수 |
| `status` | 운영 상태 | `NORMAL`, `WATCH`, `ALARM` |

### 5.1 운영 지표 용어

#### Send-out

터미널에서 외부 배관망이나 수요처로 송출한 천연가스의 양입니다.

- 컬럼: `sendout_mmscfd`
- 단위: `mmscfd`
- 분석 예시: 전체 송출량, 터미널별 송출량, 월별 송출량

#### Throughput

설비나 터미널을 통과해 처리된 에너지량입니다.

- 컬럼: `throughput_mmbtu`
- 단위: `MMBtu`
- 분석 예시: 터미널별 처리량, 기간별 처리량

#### BOG

`BOG`는 `Boil-Off Gas`의 약자입니다. LNG는 매우 낮은 온도로 저장되므로 저장·이송 중 일부가 자연적으로 기화됩니다. 이때 발생하는 증발가스를 BOG라고 합니다.

- 컬럼: `boiloff_rate_pct`
- 낮을수록 일반적으로 증발 손실 관리가 양호합니다.

#### Uptime

설비가 정상적으로 운영된 비율입니다.

- 컬럼: `uptime_pct`
- 단위: `%`
- 높을수록 운영 안정성이 좋습니다.

#### Downtime

설비가 중단되어 있던 시간입니다.

- 컬럼: `downtime_hours`
- 단위: 시간
- 낮을수록 좋습니다.

### 5.2 유지보수와 상태 값

| 컬럼 | 값 | 의미 |
|---|---|---|
| `maintenance_type` | `NONE` | 해당 기록에 유지보수 없음 |
| `maintenance_type` | `PREVENTIVE` | 고장을 예방하기 위한 정비 |
| `maintenance_type` | `CORRECTIVE` | 고장·이상 발생 후 수행한 교정정비 |
| `maintenance_type` | `INSPECTION` | 점검 또는 검사 |
| `status` | `NORMAL` | 정상 운영 |
| `status` | `WATCH` | 관찰 또는 확인 필요 |
| `status` | `ALARM` | 알람 또는 이상 상태 |

## 6. 테이블 간 관계

관계형으로 표현하면 다음과 같습니다.

```text
sites
  site_id (1)
       │
       └──────────────< assets
                         asset_id
                         site_id
                              │
                              └──────< operations
                                       asset_id
                                       site_id
```

실제 Gold 테이블에서는 다음 조건으로 데이터를 연결합니다.

```sql
operations.site_id = sites.site_id
operations.asset_id = assets.asset_id
operations.site_id = assets.site_id
```

터미널과 설비를 별도 테이블로 나눈 것은 다음을 보여주기 위해서입니다.

- 기준 정보와 실적 데이터의 분리
- 여러 테이블 간 조인
- Unity Catalog 객체 관리
- Silver 정제와 Gold 분석 모델링

## 7. 메달리온 아키텍처에서의 데이터 변화

### 7.1 Bronze

원본 CSV를 거의 그대로 적재합니다.

```text
bronze_sites
bronze_assets
bronze_operations
```

Bronze에는 원본 컬럼 외에 다음 관리 컬럼이 추가됩니다.

| 컬럼 | 의미 |
|---|---|
| `_source_file` | 데이터가 들어온 원본 파일 경로 |
| `_ingested_at` | Databricks가 데이터를 적재한 시각 |

Bronze의 목적은 원본 보존과 재처리입니다. 분석을 위한 복잡한 변환은 최소화합니다.

### 7.2 Silver

Silver에서는 분석 가능한 형태로 데이터를 정제합니다.

```text
silver_sites
silver_assets
silver_operations_clean
```

주요 정제 내용은 다음과 같습니다.

- 문자열 앞뒤 공백 제거
- `operation_ts`를 TIMESTAMP로 변환
- 날짜를 DATE로 변환
- 숫자 컬럼을 DOUBLE 또는 INT로 변환
- `terminal_type`, `status` 등을 대문자로 통일
- `operation_id` 기준 중복 제거
- 송출량·중단 시간 음수 제거
- BOG 비율과 가동률을 0~100 범위로 검증
- 유지보수 유형과 상태 값 검증

파이프라인에는 데이터 품질 조건이 선언되어 있습니다. 예를 들어 `operation_id`가 없거나 가동률이 100을 초과하면 해당 행을 분석 데이터에서 제외합니다.

### 7.3 Gold

Gold는 대시보드·Metric View·Genie에서 직접 사용할 분석용 테이블입니다.

```text
gold_lng_operations
```

운영 기록에 다음 기준 정보를 결합합니다.

- 터미널명
- 국가
- 권역
- 터미널 유형
- 설계 송출능력
- 설비명
- 설비 분류
- 설비 중요도

따라서 사용자는 여러 테이블을 직접 조인하지 않고도 다음과 같은 질문을 할 수 있습니다.

```text
터미널별 평균 가동률을 비교해줘.
중요도가 높은 설비 중 다운타임이 가장 긴 설비는 무엇이야?
국가별 총 송출량을 보여줘.
```

## 8. Metric View에서 제공하는 대표 측정값

`lng_operations_metrics`는 `gold_lng_operations` 위에 만드는 Metric View입니다.

| 측정값 | 계산 방식 | 의미 |
|---|---|---|
| `total_sendout_mmscfd` | `SUM(sendout_mmscfd)` | 총 송출량 |
| `average_uptime_pct` | `AVG(uptime_pct)` | 평균 가동률 |
| `average_boiloff_rate_pct` | `AVG(boiloff_rate_pct)` | 평균 BOG 비율 |
| `total_downtime_hours` | `SUM(downtime_hours)` | 총 중단 시간 |
| `total_maintenance_cost_usd` | `SUM(maintenance_cost_usd)` | 총 유지보수 비용 |
| `incident_count` | `SUM(incident_count)` | 사고 건수 |
| `alarm_operation_count` | `ALARM` 행의 합계 | 알람 기록 수 |
| `corrective_maintenance_cost_usd` | `CORRECTIVE` 비용 합계 | 교정정비 비용 |

Metric View에는 사용자가 질문할 때 활용할 한글 표시명과 동의어도 정의합니다.

예를 들어 다음 표현은 모두 `total_sendout_mmscfd`로 연결할 수 있습니다.

```text
송출량
공급량
send-out
send out
가스 공급량
```

## 9. Genie에서 사용할 수 있는 대표 질문

### 기본 질문

```text
전체 기간의 총 send-out은 얼마야?
터미널별 평균 가동률을 비교해줘.
설비별 유지보수 비용을 보여줘.
```

### 시간 분석 질문

```text
월별 send-out 추이를 보여줘.
일자별 평균 가동률을 보여줘.
최근 기간의 다운타임 변화를 보여줘.
```

### 운영·유지보수 질문

```text
BOG 비율이 가장 높은 설비는 무엇이야?
ALARM 상태의 운영 기록을 보여줘.
CORRECTIVE 유지보수 비용이 가장 높은 터미널은 어디야?
```

## 10. AI Search 용어집

`glossary.csv`는 자연어 질문에서 발생할 수 있는 전문 용어와 동의어를 관리합니다.

예를 들어 다음과 같은 표현을 표준 용어로 연결합니다.

| 사용자가 말하는 표현 | 표준 용어 |
|---|---|
| 액화천연가스 | LNG |
| 기화 | Regasification |
| 재기화 | Regasification |
| 증발가스 | BOG |
| boil off gas | BOG |
| 송출량 | `total_sendout_mmscfd` |
| 가동률 | `average_uptime_pct` |

AI Search는 이 용어집을 사용해 전문 용어의 정의, 동의어, 권장 사용법을 검색합니다.

## 11. 검증용 지원 파일

### `expected_results.csv`

파이프라인이 정상적으로 실행되었는지 확인할 때 사용합니다.

| 검증 항목 | 기대값 |
|---|---:|
| 전체 운영 기록 | 300건 |
| 터미널 수 | 4개 |
| 설비 수 | 12개 |

### `genie_benchmarks.csv`

Genie가 질문을 올바르게 이해했는지 비교할 기준입니다.

예를 들어 다음을 확인합니다.

- 전체 송출량 질문이 총합 측정값을 사용하는가
- 터미널별 질문이 `site_name`으로 그룹화되는가
- 월별 질문이 `operation_month` 순서로 정렬되는가

### `agent_evaluation.csv`

Supervisor Agent가 질문을 적절한 하위 Agent로 전달하는지 확인합니다.

| 질문 유형 | 기대 경로 |
|---|---|
| 터미널별 평균 가동률 | Genie Agent |
| BOG 용어 설명 | AI Search |
| 대시보드 생성 요청 | Genie Agent 또는 Dashboard 경로 |

## 12. Databricks에서 최종적으로 보이는 구조

```text
Catalog: issu_dip_wksp
├─ Schema: gasentec_landing
│  └─ Volume: raw
│     ├─ sites.csv
│     ├─ assets.csv
│     └─ operations/
│        ├─ operations_batch_001.csv
│        ├─ operations_batch_002.csv
│        └─ operations_batch_003.csv
└─ Schema: gasentec_hands_on
   ├─ bronze_sites
   ├─ bronze_assets
   ├─ bronze_operations
   ├─ silver_sites
   ├─ silver_assets
   ├─ silver_operations_clean
   ├─ gold_lng_operations
   └─ lng_operations_metrics
```

지원 CSV와 PDF는 이후 Genie, AI Search, Knowledge Assistant, Supervisor Agent 데모에서 사용합니다.

## 13. 이 데이터로 보여줄 수 있는 데모 흐름

```text
CSV 파일 업로드
    ↓
Volume에 원천 파일 저장
    ↓
Lakeflow Declarative Pipeline 실행
    ↓
Bronze → Silver → Gold 생성
    ↓
Gold 기반 Metric View 생성
    ↓
Genie Code로 AI/BI 대시보드 생성
    ↓
Ask Genie 질문 실행
    ↓
Genie Agent와 AI Search 연동
    ↓
Knowledge Assistant·Supervisor·Databricks Apps 시연
```

이 구조를 사용하면 하나의 작은 데이터셋으로 데이터 엔지니어링, 의미 계층, 자연어 분석, 용어 검색, Agent 라우팅을 한 번에 설명할 수 있습니다.
