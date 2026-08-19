SELECT 'bronze_sites' AS table_name, COUNT(*) AS row_count
FROM issu_dip_wksp.gasentec_hands_on.bronze_sites
UNION ALL
SELECT 'bronze_assets', COUNT(*)
FROM issu_dip_wksp.gasentec_hands_on.bronze_assets
UNION ALL
SELECT 'bronze_operations', COUNT(*)
FROM issu_dip_wksp.gasentec_hands_on.bronze_operations
UNION ALL
SELECT 'gold_lng_operations', COUNT(*)
FROM issu_dip_wksp.gasentec_hands_on.gold_lng_operations;

SELECT
  COUNT(*) AS operation_count,
  COUNT(DISTINCT site_id) AS site_count,
  COUNT(DISTINCT asset_id) AS asset_count,
  ROUND(SUM(sendout_mmscfd), 2) AS total_sendout_mmscfd,
  ROUND(AVG(uptime_pct), 2) AS average_uptime_pct,
  ROUND(SUM(maintenance_cost_usd), 2) AS total_maintenance_cost_usd,
  SUM(CASE WHEN status = 'ALARM' THEN 1 ELSE 0 END) AS alarm_operation_count
FROM issu_dip_wksp.gasentec_hands_on.gold_lng_operations;
