"""Generate the small, deterministic synthetic dataset used by the GasEntec demo.

The rows are fictional and are inspired only by publicly described LNG solution
categories.  They are not GasEntec customer, project, or operating data.
"""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "sample_data" / "raw"
SUPPORT = ROOT / "sample_data" / "support"


def write_csv(relative_path: str, fieldnames: list[str], rows: list[dict]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rng = random.Random(20260819)

    sites = [
        {
            "site_id": "S001",
            "site_name": "Philippines Hybrid Terminal (Demo)",
            "country": "Philippines",
            "region": "Asia",
            "terminal_type": "HYBRID",
            "commissioned_date": "2021-06-01",
            "design_sendout_mmscfd": 500,
            "site_status": "ACTIVE",
        },
        {
            "site_id": "S002",
            "site_name": "Bali Small-Scale FRU (Demo)",
            "country": "Indonesia",
            "region": "Asia",
            "terminal_type": "FLOATING",
            "commissioned_date": "2020-09-15",
            "design_sendout_mmscfd": 120,
            "site_status": "ACTIVE",
        },
        {
            "site_id": "S003",
            "site_name": "Aqaba Onshore Terminal (Demo)",
            "country": "Jordan",
            "region": "Middle East",
            "terminal_type": "ONSHORE",
            "commissioned_date": "2024-11-01",
            "design_sendout_mmscfd": 720,
            "site_status": "ACTIVE",
        },
        {
            "site_id": "S004",
            "site_name": "Dakar Jetty Regas Unit (Demo)",
            "country": "Senegal",
            "region": "Africa",
            "terminal_type": "JETTY",
            "commissioned_date": "2025-04-01",
            "design_sendout_mmscfd": 300,
            "site_status": "ACTIVE",
        },
    ]

    assets = [
        {"asset_id": "A001", "site_id": "S001", "asset_name": "RegasTainer Module 01", "asset_category": "REGASIFICATION", "criticality": "HIGH"},
        {"asset_id": "A002", "site_id": "S001", "asset_name": "BOG Compressor 01", "asset_category": "BOG_MANAGEMENT", "criticality": "HIGH"},
        {"asset_id": "A003", "site_id": "S001", "asset_name": "Cargo Handling Arm 01", "asset_category": "CARGO_HANDLING", "criticality": "MEDIUM"},
        {"asset_id": "A004", "site_id": "S002", "asset_name": "FRU Regas Module 01", "asset_category": "REGASIFICATION", "criticality": "HIGH"},
        {"asset_id": "A005", "site_id": "S002", "asset_name": "Cold Tech Skid 01", "asset_category": "COLD_TECH", "criticality": "MEDIUM"},
        {"asset_id": "A006", "site_id": "S002", "asset_name": "Pressure Management Unit 01", "asset_category": "PRESSURE_MANAGEMENT", "criticality": "HIGH"},
        {"asset_id": "A007", "site_id": "S003", "asset_name": "Onshore Vaporizer 01", "asset_category": "REGASIFICATION", "criticality": "HIGH"},
        {"asset_id": "A008", "site_id": "S003", "asset_name": "Re-liquefaction Box 01", "asset_category": "RELIQUEFACTION", "criticality": "MEDIUM"},
        {"asset_id": "A009", "site_id": "S003", "asset_name": "Cargo Handling Arm 02", "asset_category": "CARGO_HANDLING", "criticality": "MEDIUM"},
        {"asset_id": "A010", "site_id": "S004", "asset_name": "Jetty Regas Module 01", "asset_category": "REGASIFICATION", "criticality": "HIGH"},
        {"asset_id": "A011", "site_id": "S004", "asset_name": "BOG Compressor 02", "asset_category": "BOG_MANAGEMENT", "criticality": "HIGH"},
        {"asset_id": "A012", "site_id": "S004", "asset_name": "Truck Loading Bay 01", "asset_category": "CARGO_HANDLING", "criticality": "MEDIUM"},
    ]

    write_csv(
        "sample_data/raw/sites.csv",
        list(sites[0].keys()),
        sites,
    )
    write_csv(
        "sample_data/raw/assets.csv",
        list(assets[0].keys()),
        assets,
    )

    site_by_id = {row["site_id"]: row for row in sites}
    assets_by_site: dict[str, list[dict]] = {}
    for asset in assets:
        assets_by_site.setdefault(asset["site_id"], []).append(asset)

    operation_fields = [
        "operation_id",
        "operation_ts",
        "site_id",
        "asset_id",
        "shift",
        "sendout_mmscfd",
        "throughput_mmbtu",
        "boiloff_rate_pct",
        "uptime_pct",
        "downtime_hours",
        "maintenance_type",
        "maintenance_cost_usd",
        "incident_count",
        "status",
    ]
    all_operations: list[dict] = []
    start = datetime(2026, 1, 1, 0, 0, 0)
    for index in range(300):
        site = sites[index % len(sites)]
        site_assets = assets_by_site[site["site_id"]]
        asset = site_assets[(index // len(sites)) % len(site_assets)]
        timestamp = start + timedelta(days=(index * 2) % 180, hours=(index * 4) % 24)
        hour = timestamp.hour
        shift = "DAY" if 8 <= hour < 20 else "NIGHT"

        design = float(site["design_sendout_mmscfd"])
        sendout = round(design * (0.68 + rng.random() * 0.27), 2)
        throughput = round(sendout * (24.0 + rng.random() * 3.0) * 52.0, 2)
        boiloff = round(0.12 + rng.random() * 0.58, 3)
        uptime = round(98.8 - rng.random() * 3.2, 2)

        if index % 29 == 0:
            maintenance_type = "CORRECTIVE"
            downtime = round(2.0 + rng.random() * 5.0, 2)
            maintenance_cost = round(18000 + rng.random() * 42000, 2)
        elif index % 11 == 0:
            maintenance_type = "INSPECTION"
            downtime = round(0.2 + rng.random() * 1.0, 2)
            maintenance_cost = round(1200 + rng.random() * 3500, 2)
        elif index % 7 == 0:
            maintenance_type = "PREVENTIVE"
            downtime = round(0.5 + rng.random() * 1.8, 2)
            maintenance_cost = round(4000 + rng.random() * 10000, 2)
        else:
            maintenance_type = "NONE"
            downtime = round(rng.random() * 0.25, 2)
            maintenance_cost = 0.0

        incident_count = 1 if index % 47 == 0 else 0
        status = "ALARM" if incident_count else ("WATCH" if downtime >= 2.0 else "NORMAL")
        all_operations.append(
            {
                "operation_id": f"OP{index + 1:05d}",
                "operation_ts": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "site_id": site["site_id"],
                "asset_id": asset["asset_id"],
                "shift": shift,
                "sendout_mmscfd": sendout,
                "throughput_mmbtu": throughput,
                "boiloff_rate_pct": boiloff,
                "uptime_pct": uptime,
                "downtime_hours": downtime,
                "maintenance_type": maintenance_type,
                "maintenance_cost_usd": maintenance_cost,
                "incident_count": incident_count,
                "status": status,
            }
        )

    for batch in range(3):
        start_index = batch * 100
        write_csv(
            f"sample_data/raw/operations/operations_batch_{batch + 1:03d}.csv",
            operation_fields,
            all_operations[start_index : start_index + 100],
        )

    glossary_base = [
        ("LNG", "액화천연가스. 천연가스를 극저온에서 액화해 저장·운송하는 연료", "LNG", "액화천연가스|liquefied natural gas", "터미널별 LNG 운영 현황을 보여줘", "액화천연가스", "용어 정의를 우선 사용"),
        ("Regasification", "액화 상태의 LNG를 기화해 천연가스로 전환하는 공정", "재기화", "regas|기화", "재기화 설비의 가동률은 얼마야?", "재기화", "기화·재기화는 Regasification으로 통일"),
        ("BOG", "저장·이송 중 자연 기화되는 LNG 증발가스(Boil-Off Gas)", "BOG", "증발가스|boil off gas", "BOG 비율이 가장 높은 설비는?", "평균 BOG 비율", "BOG rate가 낮을수록 일반적으로 양호"),
        ("FSRU", "LNG를 저장하고 재기화하는 부유식 저장·재기화 설비", "FSRU", "부유식 저장 재기화 설비", "부유식 터미널과 육상 터미널을 비교해줘", "부유식 저장·재기화 설비", "FRU·FSU와 혼동하면 기능을 확인"),
        ("Send-out", "터미널에서 기화 후 외부로 공급하는 천연가스 유량", "send-out", "공급량|송출량", "월별 send-out 추이를 보여줘", "총 send-out", "송출량·공급량은 total_sendout_mmscfd"),
        ("Preventive maintenance", "고장 전에 계획적으로 수행하는 예방정비", "예방정비", "PM|planned maintenance", "예방정비 비중을 계산해줘", "예방정비", "maintenance_type = PREVENTIVE"),
        ("Corrective maintenance", "고장이나 이상 발생 후 복구를 위해 수행하는 교정정비", "교정정비", "CM|breakdown maintenance", "교정정비 비용이 높은 사이트는?", "교정정비", "maintenance_type = CORRECTIVE"),
        ("O&M", "터미널과 설비의 운영 및 유지보수(Operation & Maintenance)", "O&M", "운영유지보수|운영 및 유지보수", "O&M 비용을 설비 유형별로 나눠줘", "운영 및 유지보수", "운영·정비 비용과 다운타임을 함께 확인"),
    ]
    glossary = [
        {
            "term_id": f"T{i + 1:03d}",
            "term": term,
            "definition": definition,
            "preferred_usage": preferred_usage,
            "aliases": aliases,
            "example_question": example_question,
            "metric_or_field": metric_or_field,
            "resolution_rule": resolution_rule,
            "search_text": " ".join([term, definition, preferred_usage, aliases, example_question]),
        }
        for i, (term, definition, preferred_usage, aliases, example_question, metric_or_field, resolution_rule) in enumerate(glossary_base)
    ]
    write_csv("sample_data/support/glossary.csv", list(glossary[0].keys()), glossary)

    examples = [
        {"example_id": "E001", "category": "기본", "question": "전체 기간의 총 send-out은 얼마야?", "sql_answer": "SELECT MEASURE(total_sendout_mmscfd) AS total_sendout_mmscfd FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics", "teaching_point": "기본 합계 측정값"},
        {"example_id": "E002", "category": "기본", "question": "터미널별 평균 가동률을 비교해줘", "sql_answer": "SELECT site_name, MEASURE(average_uptime_pct) AS average_uptime_pct FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics GROUP BY site_name ORDER BY average_uptime_pct DESC", "teaching_point": "사이트 차원과 평균 측정값"},
        {"example_id": "E003", "category": "분석", "question": "월별 send-out 추이를 보여줘", "sql_answer": "SELECT operation_month, MEASURE(total_sendout_mmscfd) AS total_sendout_mmscfd FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics GROUP BY operation_month ORDER BY operation_month", "teaching_point": "시간 차원 추이"},
        {"example_id": "E004", "category": "분석", "question": "설비 유형별 다운타임과 유지보수 비용을 비교해줘", "sql_answer": "SELECT asset_category, MEASURE(total_downtime_hours) AS total_downtime_hours, MEASURE(total_maintenance_cost_usd) AS total_maintenance_cost_usd FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics GROUP BY asset_category ORDER BY total_downtime_hours DESC", "teaching_point": "복수 측정값 비교"},
        {"example_id": "E005", "category": "분석", "question": "BOG 비율이 높은 상위 3개 설비를 보여줘", "sql_answer": "SELECT asset_name, MEASURE(average_boiloff_rate_pct) AS average_boiloff_rate_pct FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics GROUP BY asset_name ORDER BY average_boiloff_rate_pct DESC LIMIT 3", "teaching_point": "평균값과 상위 N"},
        {"example_id": "E006", "category": "운영", "question": "교정정비 비용이 가장 높은 터미널은 어디야?", "sql_answer": "SELECT site_name, MEASURE(corrective_maintenance_cost_usd) AS corrective_maintenance_cost_usd FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics GROUP BY site_name ORDER BY corrective_maintenance_cost_usd DESC LIMIT 1", "teaching_point": "조건부 합계"},
        {"example_id": "E007", "category": "안전", "question": "ALARM 상태 기록과 사고 건수를 알려줘", "sql_answer": "SELECT MEASURE(alarm_operation_count) AS alarm_operation_count, MEASURE(incident_count) AS incident_count FROM issu_dip_wksp.gasentec_hands_on.lng_operations_metrics", "teaching_point": "운영 안전 지표"},
        {"example_id": "E008", "category": "되묻기", "question": "성능이 좋은 터미널을 알려줘", "sql_answer": "Clarify whether performance means send-out, uptime, boil-off rate, downtime, or maintenance cost before querying.", "teaching_point": "다의어 질문은 기준을 먼저 확인"},
    ]
    write_csv("sample_data/support/genie_example_queries.csv", list(examples[0].keys()), examples)

    benchmarks = [
        {"benchmark_id": "B001", "question": row["question"], "expected_metric": metric, "expected_group_by": group_by, "acceptance_rule": rule}
        for row, metric, group_by, rule in [
            (examples[0], "total_sendout_mmscfd", "none", "single total returned"),
            (examples[1], "average_uptime_pct", "site_name", "four sites ranked descending"),
            (examples[2], "total_sendout_mmscfd", "operation_month", "chronological monthly series"),
            (examples[3], "total_downtime_hours,total_maintenance_cost_usd", "asset_category", "both measures returned"),
            (examples[4], "average_boiloff_rate_pct", "asset_name", "top three assets returned"),
            (examples[6], "alarm_operation_count,incident_count", "none", "safety counts returned"),
        ]
    ]
    write_csv("sample_data/support/genie_benchmarks.csv", list(benchmarks[0].keys()), benchmarks)

    data_dictionary = [
        {"layer": "bronze", "table_name": "bronze_operations", "column_name": "sendout_mmscfd", "data_type": "STRING", "definition": "원본 송출량(mmscfd)"},
        {"layer": "silver", "table_name": "silver_operations_clean", "column_name": "uptime_pct", "data_type": "DOUBLE", "definition": "0~100 범위의 가동률"},
        {"layer": "gold", "table_name": "gold_lng_operations", "column_name": "sendout_mmscfd", "data_type": "DOUBLE", "definition": "분석용 송출량 원천 컬럼. Metric View에서 total_sendout_mmscfd로 합산"},
        {"layer": "gold", "table_name": "gold_lng_operations", "column_name": "boiloff_rate_pct", "data_type": "DOUBLE", "definition": "BOG 비율(%)"},
        {"layer": "gold", "table_name": "gold_lng_operations", "column_name": "maintenance_cost_usd", "data_type": "DOUBLE", "definition": "유지보수 비용(USD)"},
        {"layer": "gold", "table_name": "gold_lng_operations", "column_name": "incident_count", "data_type": "INT", "definition": "운영 기록에 연결된 사고 건수"},
    ]
    write_csv("sample_data/support/data_dictionary.csv", list(data_dictionary[0].keys()), data_dictionary)

    agent_evaluation = [
        {"case_id": "A001", "question": "터미널별 평균 가동률을 비교해줘", "expected_route": "genie_agent", "expected_behavior": "metric view query and ranked table", "score": 1},
        {"case_id": "A002", "question": "BOG가 뭐야?", "expected_route": "ai_search", "expected_behavior": "glossary definition and alias", "score": 1},
        {"case_id": "A003", "question": "월별 send-out 추이를 대시보드로 만들어줘", "expected_route": "genie_agent", "expected_behavior": "AI/BI dashboard specification", "score": 1},
        {"case_id": "A004", "question": "성능이 좋은 터미널을 알려줘", "expected_route": "supervisor_clarify", "expected_behavior": "ask which performance metric", "score": 1},
    ]
    write_csv("sample_data/support/agent_evaluation.csv", list(agent_evaluation[0].keys()), agent_evaluation)

    totals = {
        "total_operation_records": len(all_operations),
        "total_sites": len(sites),
        "total_assets": len(assets),
        "total_sendout_mmscfd": round(sum(float(row["sendout_mmscfd"]) for row in all_operations), 2),
        "average_uptime_pct": round(sum(float(row["uptime_pct"]) for row in all_operations) / len(all_operations), 2),
        "total_maintenance_cost_usd": round(sum(float(row["maintenance_cost_usd"]) for row in all_operations), 2),
        "alarm_operation_count": sum(row["status"] == "ALARM" for row in all_operations),
    }
    expected = [
        {"metric": key, "expected_value": value, "validation_sql": "SELECT COUNT(*) FROM issu_dip_wksp.gasentec_hands_on.gold_lng_operations" if key == "total_operation_records" else "see metric view query"}
        for key, value in totals.items()
    ]
    write_csv("sample_data/support/expected_results.csv", list(expected[0].keys()), expected)

    print(f"Generated synthetic GasEntec demo data under {ROOT}")
    print(totals)


if __name__ == "__main__":
    main()
