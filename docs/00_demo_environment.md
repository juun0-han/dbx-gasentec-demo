# Demo 환경 구성: 데이터 업로드부터 Lakeflow Job까지

이 문서는 Databricks 화면에서 직접 GasEntec LNG 데모를 구성하는 순서입니다. Databricks CLI나 Bundle을 사용하지 않습니다.

## 대상 Workspace

```text
Workspace: issu-dip-wksp (Default)
Host: https://dbc-9f87ed8e-e4c2.cloud.databricks.com
Warehouse: Serverless Starter Warehouse
```

Git folder가 이미 Workspace에 생성되어 있어야 합니다. 이 문서에서 사용하는 주요 파일은 다음과 같습니다.

```text
notebooks/01_lng_demo_pipeline.sql
notebooks/04_demo_validate.sql
sample_data/raw/sites.csv
sample_data/raw/assets.csv
sample_data/raw/operations/operations_batch_001.csv
sample_data/raw/operations/operations_batch_002.csv
sample_data/raw/operations/operations_batch_003.csv
```

## 1. 기존 Catalog에서 Schema 만들기

이 Workspace에서는 별도 Catalog를 만들지 않고 이미 있는 `issu_dip_wksp` Catalog를 사용합니다.

1. 왼쪽 메뉴에서 **Catalog**를 엽니다.
2. 기존 Catalog인 `issu_dip_wksp`를 엽니다.
3. 다음 Schema가 이미 있으면 그대로 사용하고, 없으면 **Create schema**로 각각 생성합니다.

```text
gasentec_landing
gasentec_hands_on
```

## 2. Volume 만들기

1. `issu_dip_wksp > gasentec_landing`으로 이동합니다.
2. **Create > Volume**을 선택합니다.
3. Volume 이름을 `raw`로 입력합니다.
4. Volume 유형은 **Managed volume**을 사용합니다.
5. Volume을 생성합니다.

최종 경로는 다음과 같습니다.

```text
/Volumes/issu_dip_wksp/gasentec_landing/raw
```

## 3. 원천 CSV 업로드하기

Pipeline은 다음 Volume 경로를 읽습니다.

```text
/Volumes/issu_dip_wksp/gasentec_landing/raw/sites*.csv
/Volumes/issu_dip_wksp/gasentec_landing/raw/assets*.csv
/Volumes/issu_dip_wksp/gasentec_landing/raw/operations
```

`raw` Volume을 열고 **Upload files**로 `sites.csv`와 `assets.csv`를 Volume 바로 아래에 업로드합니다.

그 다음 `raw` Volume에서 **Create folder**로 `operations` 폴더를 만들고, 해당 폴더에 다음 세 파일을 업로드합니다.

```text
operations_batch_001.csv
operations_batch_002.csv
operations_batch_003.csv
```

업로드 후 구조는 다음과 같아야 합니다.

```text
raw/
├─ sites.csv
├─ assets.csv
└─ operations/
   ├─ operations_batch_001.csv
   ├─ operations_batch_002.csv
   └─ operations_batch_003.csv
```

처음 Pipeline만 실행할 때는 `sample_data/support` 파일을 업로드하지 않아도 됩니다.

## 4. Lakeflow Declarative Pipeline 만들기

1. 왼쪽 메뉴에서 **Jobs & Pipelines**를 엽니다.
2. **Pipelines** 탭을 선택합니다.
3. **Create pipeline** 또는 **ETL pipeline**을 선택합니다.
4. 아래 표와 같이 입력합니다.

| 항목 | 입력값 |
|---|---|
| Pipeline name | `gasentec_lng_demo_pipeline` |
| Pipeline mode | `Triggered` |
| Pipeline type | `ETL` 또는 `Lakeflow Declarative Pipeline` |
| Catalog | `issu_dip_wksp` |
| Target schema | `gasentec_hands_on` |
| Compute | `Serverless` 또는 기본 Pipeline compute |

5. **Source code** 영역에서 Git folder의 다음 파일을 추가합니다.

```text
notebooks/01_lng_demo_pipeline.sql
```

6. Pipeline을 저장합니다.

Pipeline 소스에는 다음 데이터셋이 선언되어 있습니다.

```text
bronze_sites
bronze_assets
bronze_operations
silver_sites
silver_assets
silver_operations_clean
gold_lng_operations
```

## 5. Pipeline 실행

1. Pipeline 화면에서 **Start** 또는 **Run now**를 선택합니다.
2. 실행이 끝날 때까지 기다립니다.
3. 그래프에서 Bronze → Silver → Gold 흐름을 확인합니다.
4. 각 데이터셋을 클릭해 입력 행 수와 품질 규칙 결과를 확인합니다.

정상 실행 후 예상 건수는 다음과 같습니다.

```text
bronze_sites: 4
bronze_assets: 12
bronze_operations: 300
gold_lng_operations: 300
```

## 6. Lakeflow Job 만들기

Pipeline을 정해진 순서로 실행하고 성공 여부를 관리하려면 Job에 Pipeline task를 추가합니다.

1. 왼쪽 메뉴에서 **Jobs & Pipelines**를 엽니다.
2. **Jobs** 탭을 선택합니다.
3. **Create job**을 선택합니다.
4. Job 이름을 다음과 같이 입력합니다.

```text
gasentec_lng_demo_refresh_job
```

5. 첫 번째 Task를 다음과 같이 설정합니다.

```text
Task name: run_medallion_pipeline
Task type: Pipeline
Pipeline: gasentec_lng_demo_pipeline
```

Pipeline task에서는 별도 클러스터를 만들지 않고 Pipeline에 설정된 Serverless compute를 사용합니다. Pipeline task는 Pipeline의 소스 코드와 compute 설정을 그대로 사용합니다.

6. 데모에서는 Schedule을 설정하지 않고 **Manual** 실행으로 둡니다.
7. **Create** 또는 **Save**를 선택합니다.

## 7. Job 실행 확인

1. `gasentec_lng_demo_refresh_job` 화면에서 **Run now**를 선택합니다.
2. Task 상태가 다음 순서로 진행되는지 확인합니다.

```text
Pending → Running → Successful
```

3. `run_medallion_pipeline` Task를 열어 Pipeline 실행 링크를 확인합니다.
4. Pipeline 화면에서 Bronze → Silver → Gold 그래프를 다시 확인합니다.

Job은 여러 Task 간 의존성을 관리하고, Pipeline은 데이터셋 간 변환 의존성을 관리합니다.

## 8. 선택 사항: 검증 Task 추가하기

Pipeline 실행 후 행 수를 자동으로 확인하려면 Job에 두 번째 Task를 추가할 수 있습니다.

```text
Task name: validate_pipeline
Task type: Notebook
Notebook path: notebooks/04_demo_validate.sql
Depends on: run_medallion_pipeline
```

SQL Task의 **File** 유형을 사용하는 화면이라면 `resources/sql/validate_pipeline.sql`을 선택할 수도 있습니다. 이 경우 SQL Warehouse로 `Serverless Starter Warehouse`를 선택합니다.

## 9. 완료 기준

```text
[ ] 기존 issu_dip_wksp Catalog 확인
[ ] gasentec_landing Schema 생성
[ ] gasentec_hands_on Schema 생성
[ ] gasentec_landing.raw Volume 생성
[ ] sites.csv 업로드
[ ] assets.csv 업로드
[ ] operations 배치 3개 업로드
[ ] gasentec_lng_demo_pipeline 생성
[ ] Pipeline 성공 실행
[ ] gasentec_lng_demo_refresh_job 생성
[ ] Job의 run_medallion_pipeline Task 성공 실행
```

완료 후 다음 단계에서 Gold 테이블을 기반으로 Metric View를 생성합니다.
