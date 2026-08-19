-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 03. LNG 운영 Metric View 의미·성능 최적화
-- MAGIC
-- MAGIC 업무 용어 설명, 동의어, 단위·표시 형식, 일 단위 Materialization을 추가합니다.

-- COMMAND ----------

CREATE OR REPLACE VIEW issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
WITH METRICS
LANGUAGE YAML
AS
$$
version: 1.1
comment: '합성 LNG 터미널 운영 및 O&M 기록을 위한 표준 Metric View'
source: issu_dip_wksp.gasentec_hands_on.gold_lng_operations
fields:
  - name: operation_date
    expr: operation_date
    display_name: '운영일'
    comment: '운영 기록의 달력 날짜'
    synonyms: ['운영 날짜', '일자', '날짜']
  - name: operation_month
    expr: operation_month
    display_name: '운영월'
    comment: '운영일을 월 단위로 묶은 시간 차원'
    synonyms: ['월', '월별', '기간']
  - name: site_name
    expr: site_name
    display_name: '터미널명'
    comment: '합성 데모 터미널의 이름'
    synonyms: ['사이트', '프로젝트', '터미널', '현장']
  - name: country
    expr: country
    display_name: '국가'
    comment: '터미널이 위치한 국가'
    synonyms: ['국가명', '국가별']
  - name: region
    expr: region
    display_name: '권역'
    comment: 'Asia, Middle East, Africa 등 지역 권역'
    synonyms: ['지역', '대륙', '권역별']
  - name: terminal_type
    expr: terminal_type
    display_name: '터미널 유형'
    comment: 'HYBRID, FLOATING, ONSHORE, JETTY 중 하나'
    synonyms: ['터미널 형태', '설치 유형', '인프라 유형']
  - name: asset_name
    expr: asset_name
    display_name: '설비명'
    comment: '운영 기록에 연결된 설비의 이름'
    synonyms: ['장비', '기기', '설비']
  - name: asset_category
    expr: asset_category
    display_name: '설비 카테고리'
    comment: 'REGASIFICATION, BOG_MANAGEMENT, CARGO_HANDLING, COLD_TECH, PRESSURE_MANAGEMENT, RELIQUEFACTION 중 하나'
    synonyms: ['설비 유형', '장비 유형', '제품군']
  - name: criticality
    expr: criticality
    display_name: '중요도'
    comment: '설비 장애가 운영에 미치는 중요도'
    synonyms: ['설비 중요도', 'criticality']
  - name: shift
    expr: shift
    display_name: '교대'
    comment: 'DAY 또는 NIGHT'
    synonyms: ['근무 교대', '주야간']
  - name: maintenance_type
    expr: maintenance_type
    display_name: '유지보수 유형'
    comment: 'NONE, PREVENTIVE, CORRECTIVE, INSPECTION 중 하나'
    synonyms: ['정비 유형', 'O&M 유형', '보수 구분']
  - name: status
    expr: status
    display_name: '운영 상태'
    comment: 'NORMAL, WATCH, ALARM 중 하나'
    synonyms: ['상태', '알람 상태', '운영 알림']
measures:
  - name: total_sendout_mmscfd
    expr: SUM(sendout_mmscfd)
    display_name: '총 send-out'
    comment: '터미널에서 외부로 송출한 천연가스 유량의 합계. 단위는 mmscfd이며, 사용자가 공급량·송출량·send-out이라고 말하면 이 측정값을 사용한다.'
    synonyms: ['송출량', '공급량', 'send out', '가스 공급량']
    format:
      type: number
      decimal_places: { type: exact, places: 2 }
  - name: average_uptime_pct
    expr: AVG(uptime_pct)
    display_name: '평균 가동률'
    comment: '운영 기록의 uptime_pct 평균. 백분율 값이며 높을수록 설비 가동 상태가 좋다.'
    synonyms: ['가동률', '운영률', 'uptime', 'availability']
    format:
      type: number
      decimal_places: { type: exact, places: 2 }
  - name: average_boiloff_rate_pct
    expr: AVG(boiloff_rate_pct)
    display_name: '평균 BOG 비율'
    comment: '저장·이송 중 증발한 LNG 비율의 평균. 낮을수록 증발 손실 관리가 양호하다.'
    synonyms: ['BOG 비율', '증발가스 비율', 'boil off rate']
    format:
      type: number
      decimal_places: { type: exact, places: 3 }
  - name: total_downtime_hours
    expr: SUM(downtime_hours)
    display_name: '총 다운타임'
    comment: '운영 기록에서 발생한 설비 중단 시간의 합계. 단위는 시간이다.'
    synonyms: ['중단 시간', '비가동 시간', '정지 시간']
    format:
      type: number
      decimal_places: { type: exact, places: 2 }
  - name: total_maintenance_cost_usd
    expr: SUM(maintenance_cost_usd)
    display_name: '총 유지보수 비용'
    comment: '예방정비·교정정비·검사에 사용한 비용의 합계. 단위는 USD이다.'
    synonyms: ['O&M 비용', '정비 비용', '유지보수비', 'maintenance cost']
    format:
      type: currency
      currency_code: USD
      decimal_places: { type: exact, places: 2 }
  - name: incident_count
    expr: SUM(incident_count)
    display_name: '사고 건수'
    comment: '운영 기록에 등록된 사고 건수 합계'
    synonyms: ['사고 수', 'incident', '안전 사고']
    format:
      type: number
      decimal_places: { type: exact, places: 0 }
  - name: alarm_operation_count
    expr: SUM(CASE WHEN status = 'ALARM' THEN 1 ELSE 0 END)
    display_name: 'ALARM 기록 수'
    comment: '운영 상태가 ALARM인 기록의 개수'
    synonyms: ['알람 건수', '경보 건수', 'alarm count']
    format:
      type: number
      decimal_places: { type: exact, places: 0 }
  - name: corrective_maintenance_cost_usd
    expr: SUM(CASE WHEN maintenance_type = 'CORRECTIVE' THEN maintenance_cost_usd ELSE 0 END)
    display_name: '교정정비 비용'
    comment: '고장·이상 발생 후 수행한 CORRECTIVE 정비 비용의 합계'
    synonyms: ['고장 정비 비용', 'CM 비용', 'corrective maintenance cost']
    format:
      type: currency
      currency_code: USD
      decimal_places: { type: exact, places: 2 }
materialization:
  schedule: every 1 day
  mode: relaxed
  materialized_views:
    - name: daily_site_asset
      type: aggregated
      dimensions:
        - operation_date
        - site_name
        - asset_category
      measures:
        - total_sendout_mmscfd
        - average_uptime_pct
        - average_boiloff_rate_pct
        - total_downtime_hours
        - total_maintenance_cost_usd
        - incident_count
      cluster_by:
        auto: true
$$;

-- COMMAND ----------

DESCRIBE EXTENDED issu_dip_wksp.gasentec_hands_on.lng_operations_metrics;
