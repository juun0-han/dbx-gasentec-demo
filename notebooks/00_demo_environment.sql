-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 00. GasEntec LNG Demo 환경 준비

-- COMMAND ----------

CREATE SCHEMA IF NOT EXISTS issu_dip_wksp.gasentec_landing
COMMENT 'GasEntec LNG 합성 원천 파일용 스키마';

CREATE SCHEMA IF NOT EXISTS issu_dip_wksp.gasentec_hands_on
COMMENT 'GasEntec LNG Bronze, Silver, Gold, Metric View용 스키마';

CREATE VOLUME IF NOT EXISTS issu_dip_wksp.gasentec_landing.raw
COMMENT 'GasEntec LNG Demo CSV 업로드 볼륨';

-- COMMAND ----------

LIST '/Volumes/issu_dip_wksp/gasentec_landing/raw';
LIST '/Volumes/issu_dip_wksp/gasentec_landing/raw/operations';
LIST '/Volumes/issu_dip_wksp/gasentec_landing/raw/support';

-- COMMAND ----------

SELECT
  '환경 준비 완료' AS status,
  '/Volumes/issu_dip_wksp/gasentec_landing/raw' AS upload_path,
  'issu_dip_wksp.gasentec_hands_on' AS target_schema;
