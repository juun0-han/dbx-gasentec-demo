CREATE SCHEMA IF NOT EXISTS issu_dip_wksp.gasentec_landing
COMMENT 'GasEntec LNG Demo 원천 데이터 Schema';

CREATE SCHEMA IF NOT EXISTS issu_dip_wksp.gasentec_hands_on
COMMENT 'GasEntec LNG Demo 분석 객체 Schema';

CREATE VOLUME IF NOT EXISTS issu_dip_wksp.gasentec_landing.raw
COMMENT 'GasEntec LNG Demo 원천 CSV Volume';

SELECT
  'objects_ready' AS status,
  'issu_dip_wksp' AS catalog_name,
  'issu_dip_wksp.gasentec_landing.raw' AS volume_name;
