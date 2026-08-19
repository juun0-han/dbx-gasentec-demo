# Genie Example Queries

## E001 · 기본 합계

질문:

```text
전체 기간의 총 send-out은 얼마야?
```

예상 SQL:

```sql
SELECT MEASURE(total_sendout_mmscfd) AS total_sendout_mmscfd
FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics;
```

## E002 · 터미널 비교

질문:

```text
터미널별 평균 가동률을 비교해줘
```

예상 SQL:

```sql
SELECT site_name,
       MEASURE(average_uptime_pct) AS average_uptime_pct
FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
GROUP BY site_name
ORDER BY average_uptime_pct DESC;
```

## E003 · 시간 추이

질문:

```text
월별 send-out 추이를 보여줘
```

예상 SQL:

```sql
SELECT operation_month,
       MEASURE(total_sendout_mmscfd) AS total_sendout_mmscfd
FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
GROUP BY operation_month
ORDER BY operation_month;
```

## E004 · 설비 유형별 운영·비용

질문:

```text
설비 유형별 다운타임과 유지보수 비용을 비교해줘
```

예상 SQL:

```sql
SELECT asset_category,
       MEASURE(total_downtime_hours) AS total_downtime_hours,
       MEASURE(total_maintenance_cost_usd) AS total_maintenance_cost_usd
FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
GROUP BY asset_category
ORDER BY total_downtime_hours DESC;
```

## E005 · BOG 상위 설비

질문:

```text
BOG 비율이 높은 상위 3개 설비를 보여줘
```

예상 SQL:

```sql
SELECT asset_name,
       MEASURE(average_boiloff_rate_pct) AS average_boiloff_rate_pct
FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
GROUP BY asset_name
ORDER BY average_boiloff_rate_pct DESC
LIMIT 3;
```

## E006 · 교정정비 비용

질문:

```text
교정정비 비용이 가장 높은 터미널은 어디야?
```

예상 SQL:

```sql
SELECT site_name,
       MEASURE(corrective_maintenance_cost_usd) AS corrective_maintenance_cost_usd
FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
GROUP BY site_name
ORDER BY corrective_maintenance_cost_usd DESC
LIMIT 1;
```

## E007 · 안전 지표

질문:

```text
ALARM 상태 기록과 사고 건수를 알려줘
```

예상 SQL:

```sql
SELECT MEASURE(alarm_operation_count) AS alarm_operation_count,
       MEASURE(incident_count) AS incident_count
FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics;
```

## E008 · 기준 확인

질문:

```text
성능이 좋은 터미널을 알려줘
```

기대 응답:

```text
성능을 어떤 기준으로 볼까요? send-out, 평균 가동률, BOG 비율, 다운타임, 유지보수 비용 중 선택해 주세요.
```
