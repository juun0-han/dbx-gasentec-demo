# AI/BI Dashboard용 Genie Code 프롬프트

## 데이터 소스

```text
issu_dip_wksp.gasentec_hands_on.lng_operations_metrics
```

## 기본 생성 프롬프트

```text
`issu_dip_wksp.gasentec_hands_on.lng_operations_metrics` Metric View를 사용해 "GasEntec LNG Terminal Operations Overview"라는 이름의 AI/BI 대시보드를 만들어줘.

대상 사용자는 LNG 터미널 운영 및 O&M 검토 담당자야. 이 데이터는 실제 운영 데이터가 아닌 합성 데모 데이터라는 점을 대시보드 설명에 표시해줘.

다음 KPI 카드를 추가해줘.

1. 총 송출량: mmscfd 단위의 total_sendout_mmscfd 측정값
2. 평균 가동률: % 단위의 average_uptime_pct 측정값
3. 평균 BOG 비율: % 단위의 average_boiloff_rate_pct 측정값
4. 총 유지보수 비용: USD 단위의 total_maintenance_cost_usd 측정값

다음 시각화를 추가해줘.

1. operation_month별 총 송출량 월별 추이 선 그래프
2. site_name별 평균 가동률 내림차순 순위 막대 그래프
3. asset_category별 총 다운타임과 총 유지보수 비용 비교 그래프
4. site_name별 평균 BOG 비율과 평균 가동률 산점도
5. site_name과 asset_name별 ALARM 기록 수와 사고 건수 표

다음 필터를 대시보드 전체에 추가해줘.

- operation_month
- region
- terminal_type
- asset_category
- maintenance_type

원본 컬럼을 다시 집계하지 말고 Metric View에 정의된 측정값을 사용해줘. 차트 제목에 mmscfd, %, USD, 시간 단위를 표시해줘. 월별 차트는 operation_month를 시간순으로 정렬해줘.
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
