-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 01. GasEntec LNG 메달리온 Lakeflow Pipeline
-- MAGIC
-- MAGIC Lakeflow Spark Declarative Pipelines 소스로 등록합니다.
-- MAGIC Bronze → Silver → Gold 의존성과 데이터 품질 규칙을 선언합니다.

-- COMMAND ----------

CREATE OR REFRESH STREAMING TABLE bronze_sites
COMMENT '원본 터미널/프로젝트 CSV를 증분 적재한 Sites Bronze 테이블'
TBLPROPERTIES ('quality' = 'bronze')
AS
SELECT
  *,
  _metadata.file_path AS _source_file,
  current_timestamp() AS _ingested_at
FROM STREAM read_files(
  '/Volumes/issu_dip_wksp/gasentec_landing/raw/sites*.csv',
  format => 'csv',
  header => 'true',
  inferColumnTypes => 'false'
);

-- COMMAND ----------

CREATE OR REFRESH STREAMING TABLE bronze_assets
COMMENT '원본 LNG 설비 CSV를 증분 적재한 Assets Bronze 테이블'
TBLPROPERTIES ('quality' = 'bronze')
AS
SELECT
  *,
  _metadata.file_path AS _source_file,
  current_timestamp() AS _ingested_at
FROM STREAM read_files(
  '/Volumes/issu_dip_wksp/gasentec_landing/raw/assets*.csv',
  format => 'csv',
  header => 'true',
  inferColumnTypes => 'false'
);

-- COMMAND ----------

CREATE OR REFRESH STREAMING TABLE bronze_operations
COMMENT '운영·O&M 세 개 CSV 배치를 Auto Loader로 적재한 Operations Bronze 테이블'
TBLPROPERTIES ('quality' = 'bronze')
AS
SELECT
  *,
  _metadata.file_path AS _source_file,
  current_timestamp() AS _ingested_at
FROM STREAM read_files(
  '/Volumes/issu_dip_wksp/gasentec_landing/raw/operations',
  format => 'csv',
  header => 'true',
  inferColumnTypes => 'false'
);

-- COMMAND ----------

CREATE OR REFRESH MATERIALIZED VIEW silver_sites (
  CONSTRAINT valid_site_id EXPECT (site_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_site_name EXPECT (site_name IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT positive_design_capacity EXPECT (design_sendout_mmscfd > 0) ON VIOLATION DROP ROW
)
COMMENT '터미널 차원의 타입과 필수값을 정리한 Sites Silver 테이블'
TBLPROPERTIES ('quality' = 'silver')
AS
SELECT
  TRIM(site_id) AS site_id,
  TRIM(site_name) AS site_name,
  TRIM(country) AS country,
  TRIM(region) AS region,
  UPPER(TRIM(terminal_type)) AS terminal_type,
  TRY_CAST(commissioned_date AS DATE) AS commissioned_date,
  TRY_CAST(design_sendout_mmscfd AS DOUBLE) AS design_sendout_mmscfd,
  UPPER(TRIM(site_status)) AS site_status
FROM bronze_sites;

-- COMMAND ----------

CREATE OR REFRESH MATERIALIZED VIEW silver_assets (
  CONSTRAINT valid_asset_id EXPECT (asset_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_asset_name EXPECT (asset_name IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_criticality EXPECT (criticality IN ('HIGH', 'MEDIUM', 'LOW')) ON VIOLATION DROP ROW
)
COMMENT '설비 차원의 타입과 필수값을 정리한 Assets Silver 테이블'
TBLPROPERTIES ('quality' = 'silver')
AS
SELECT
  TRIM(asset_id) AS asset_id,
  TRIM(site_id) AS site_id,
  TRIM(asset_name) AS asset_name,
  UPPER(TRIM(asset_category)) AS asset_category,
  UPPER(TRIM(criticality)) AS criticality
FROM bronze_assets;

-- COMMAND ----------

CREATE OR REFRESH MATERIALIZED VIEW silver_operations_clean (
  CONSTRAINT valid_operation_id EXPECT (operation_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_operation_ts EXPECT (operation_ts IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT non_negative_sendout EXPECT (sendout_mmscfd >= 0) ON VIOLATION DROP ROW,
  CONSTRAINT valid_boiloff EXPECT (boiloff_rate_pct BETWEEN 0 AND 100) ON VIOLATION DROP ROW,
  CONSTRAINT valid_uptime EXPECT (uptime_pct BETWEEN 0 AND 100) ON VIOLATION DROP ROW,
  CONSTRAINT non_negative_downtime EXPECT (downtime_hours >= 0) ON VIOLATION DROP ROW,
  CONSTRAINT valid_maintenance EXPECT (maintenance_type IN ('NONE', 'PREVENTIVE', 'CORRECTIVE', 'INSPECTION')) ON VIOLATION DROP ROW,
  CONSTRAINT valid_status EXPECT (status IN ('NORMAL', 'WATCH', 'ALARM')) ON VIOLATION DROP ROW
)
COMMENT '운영 타입, 범위, 유지보수 상태를 표준화한 Operations Silver 테이블'
TBLPROPERTIES ('quality' = 'silver')
AS
WITH typed AS (
  SELECT
    TRIM(operation_id) AS operation_id,
    TRY_CAST(operation_ts AS TIMESTAMP) AS operation_ts,
    TRIM(site_id) AS site_id,
    TRIM(asset_id) AS asset_id,
    UPPER(TRIM(shift)) AS shift,
    TRY_CAST(sendout_mmscfd AS DOUBLE) AS sendout_mmscfd,
    TRY_CAST(throughput_mmbtu AS DOUBLE) AS throughput_mmbtu,
    TRY_CAST(boiloff_rate_pct AS DOUBLE) AS boiloff_rate_pct,
    TRY_CAST(uptime_pct AS DOUBLE) AS uptime_pct,
    TRY_CAST(downtime_hours AS DOUBLE) AS downtime_hours,
    UPPER(TRIM(maintenance_type)) AS maintenance_type,
    TRY_CAST(maintenance_cost_usd AS DOUBLE) AS maintenance_cost_usd,
    TRY_CAST(incident_count AS INT) AS incident_count,
    UPPER(TRIM(status)) AS status,
    _source_file,
    _ingested_at
  FROM bronze_operations
), deduplicated AS (
  SELECT *
  FROM typed
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY operation_id
    ORDER BY _source_file, _ingested_at
  ) = 1
)
SELECT * FROM deduplicated;

-- COMMAND ----------

CREATE OR REFRESH MATERIALIZED VIEW gold_lng_operations
CLUSTER BY AUTO
COMMENT '터미널·설비 차원을 결합한 LNG 운영 및 O&M 분석 Gold 테이블'
TBLPROPERTIES ('quality' = 'gold')
AS
SELECT
  o.operation_id,
  o.operation_ts,
  CAST(o.operation_ts AS DATE) AS operation_date,
  DATE_TRUNC('MONTH', CAST(o.operation_ts AS DATE)) AS operation_month,
  o.site_id,
  s.site_name,
  s.country,
  s.region,
  s.terminal_type,
  s.design_sendout_mmscfd,
  o.asset_id,
  a.asset_name,
  a.asset_category,
  a.criticality,
  o.shift,
  o.sendout_mmscfd,
  o.throughput_mmbtu,
  o.boiloff_rate_pct,
  o.uptime_pct,
  o.downtime_hours,
  o.maintenance_type,
  o.maintenance_cost_usd,
  o.incident_count,
  o.status
FROM silver_operations_clean o
INNER JOIN silver_sites s USING (site_id)
INNER JOIN silver_assets a USING (asset_id, site_id);
