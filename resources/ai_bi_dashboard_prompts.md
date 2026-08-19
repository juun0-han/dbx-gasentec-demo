# AI/BI Dashboard용 Genie Code 프롬프트

## 데이터 소스

```text
issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
```

## 기본 생성 프롬프트

```text
Using the metric view issu_dip_wksp.gasentec_hands_on.lng_operations_metrics, create an AI/BI dashboard named "LNG Terminal Operations Overview".

Audience: LNG terminal operations and O&M reviewers.

Add four KPI cards:
1. Total send-out (mmscfd)
2. Average uptime (%).
3. Average BOG rate (%).
4. Total maintenance cost (USD).

Add these visualizations:
1. A monthly line chart of total send-out by operation_month.
2. A ranked bar chart of average uptime by site_name.
3. A bar chart of total downtime and total maintenance cost by asset_category.
4. A scatter chart of average BOG rate versus average uptime by site_name.
5. A table of ALARM records and incident count by site_name and asset_name.

Add filters for operation_month, region, terminal_type, asset_category, and maintenance_type. Use the Metric View measures with MEASURE() and keep units visible in titles. Mark this as synthetic demonstration data in the dashboard description.
```

## 운영 검토 대시보드 프롬프트

```text
Create a second page named "O&M and Safety" from the same metric view.

Show corrective maintenance cost, preventive maintenance cost, total downtime, alarm operation count, and incident count as KPI cards or compact charts. Break down cost and downtime by site_name, asset_category, and maintenance_type. Add a monthly trend and a table sorted by alarm count descending. Keep the same filters across all tiles and display USD, hours, and percentages in the titles.
```

## 생성 후 검증 기준

```text
The KPI values must use the Metric View measures.
The monthly chart must be sorted by operation_month.
The site comparison must use site_name.
The BOG chart must label lower BOG rate as generally better.
The dashboard must expose the five requested filters.
```
