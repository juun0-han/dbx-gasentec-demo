-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 02. LNG 운영 Metric View 기준선
-- MAGIC
-- MAGIC 설명·동의어·표시 형식·Materialization을 넣기 전 기준선입니다.

-- COMMAND ----------

CREATE OR REPLACE VIEW issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
WITH METRICS
LANGUAGE YAML
AS
$$
version: 1.1
source: issu_dip_wksp.gasentec_hands_on.gold_lng_operations
fields:
  - name: operation_date
    expr: operation_date
  - name: operation_month
    expr: operation_month
  - name: site_name
    expr: site_name
  - name: country
    expr: country
  - name: region
    expr: region
  - name: terminal_type
    expr: terminal_type
  - name: asset_name
    expr: asset_name
  - name: asset_category
    expr: asset_category
  - name: criticality
    expr: criticality
  - name: shift
    expr: shift
  - name: maintenance_type
    expr: maintenance_type
  - name: status
    expr: status
measures:
  - name: total_sendout_mmscfd
    expr: SUM(sendout_mmscfd)
  - name: average_uptime_pct
    expr: AVG(uptime_pct)
  - name: average_boiloff_rate_pct
    expr: AVG(boiloff_rate_pct)
  - name: total_downtime_hours
    expr: SUM(downtime_hours)
  - name: total_maintenance_cost_usd
    expr: SUM(maintenance_cost_usd)
  - name: incident_count
    expr: SUM(incident_count)
  - name: alarm_operation_count
    expr: SUM(CASE WHEN status = 'ALARM' THEN 1 ELSE 0 END)
  - name: corrective_maintenance_cost_usd
    expr: SUM(CASE WHEN maintenance_type = 'CORRECTIVE' THEN maintenance_cost_usd ELSE 0 END)
$$;

-- COMMAND ----------

SELECT
  MEASURE(total_sendout_mmscfd) AS total_sendout_mmscfd,
  MEASURE(average_uptime_pct) AS average_uptime_pct,
  MEASURE(total_maintenance_cost_usd) AS total_maintenance_cost_usd
FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics;
