"""Build compact, retrieval-friendly PDF documents for Knowledge Assistant tests."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "output" / "pdf"
ASSET = PDF_DIR / "assets" / "lng_terminal_illustration.png"


def register_fonts() -> None:
    regular = Path(r"C:\Windows\Fonts\malgun.ttf")
    bold = Path(r"C:\Windows\Fonts\malgunbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("Malgun", str(regular)))
        pdfmetrics.registerFont(TTFont("Malgun-Bold", str(bold)))
    else:
        pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


FONT = "Malgun" if Path(r"C:\Windows\Fonts\malgun.ttf").exists() else "DejaVu"
BOLD = "Malgun-Bold" if FONT == "Malgun" else "DejaVu-Bold"


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontName=BOLD, fontSize=22, leading=29, textColor=colors.HexColor("#0B3D4F"), alignment=TA_LEFT, spaceAfter=8),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontName=FONT, fontSize=10.5, leading=16, textColor=colors.HexColor("#49636D"), spaceAfter=14),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName=BOLD, fontSize=15, leading=21, textColor=colors.HexColor("#0B3D4F"), spaceBefore=12, spaceAfter=6),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName=BOLD, fontSize=11.5, leading=17, textColor=colors.HexColor("#176B87"), spaceBefore=8, spaceAfter=4),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName=FONT, fontSize=9.2, leading=14, textColor=colors.HexColor("#20343B"), spaceAfter=6),
        "small": ParagraphStyle("small", parent=base["BodyText"], fontName=FONT, fontSize=7.8, leading=11, textColor=colors.HexColor("#49636D"), spaceAfter=3),
        "caption": ParagraphStyle("caption", parent=base["BodyText"], fontName=FONT, fontSize=8, leading=12, textColor=colors.HexColor("#49636D"), alignment=TA_CENTER, spaceBefore=3, spaceAfter=8),
        "cell": ParagraphStyle("cell", parent=base["BodyText"], fontName=FONT, fontSize=7.6, leading=10.5, textColor=colors.HexColor("#20343B")),
        "cell_bold": ParagraphStyle("cell_bold", parent=base["BodyText"], fontName=BOLD, fontSize=7.6, leading=10.5, textColor=colors.HexColor("#0B3D4F")),
        "question": ParagraphStyle("question", parent=base["BodyText"], fontName=BOLD, fontSize=9.2, leading=13, textColor=colors.HexColor("#0B3D4F"), spaceAfter=3),
    }


STYLES = make_styles()


def p(text: str, style: str = "body") -> Paragraph:
    return Paragraph(text, STYLES[style])


def table(rows, widths, header=True):
    converted = []
    for row_index, row in enumerate(rows):
        converted.append([
            Paragraph(str(value), STYLES["cell_bold" if header and row_index == 0 else "cell"])
            for value in row
        ])
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#C8D8DE")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B617D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ])
        for cell in converted[0]:
            cell.style.textColor = colors.white
    for row_index in range(1 if header else 0, len(rows)):
        if row_index % 2 == 0:
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), colors.HexColor("#F3F8FA")))
    t.setStyle(TableStyle(commands))
    return t


def banner(text: str):
    t = Table([[Paragraph(text, ParagraphStyle("banner", parent=STYLES["body"], fontName=BOLD, textColor=colors.HexColor("#0B3D4F"), spaceAfter=0))]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F3F6")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#9FC5D0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def footer(title: str):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#C8D8DE"))
        canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
        canvas.setFont(FONT, 7.5)
        canvas.setFillColor(colors.HexColor("#6B7F86"))
        canvas.drawString(18 * mm, 9 * mm, title)
        canvas.drawRightString(192 * mm, 9 * mm, f"Page {doc.page}")
        canvas.restoreState()
    return draw


def build_pdf(path: Path, title: str, subtitle: str, story) -> None:
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=19 * mm,
        title=title,
        author="Databricks GasEntec Demo",
        subject="Knowledge Assistant demo document",
    )
    full_story = [p(title, "title"), p(subtitle, "subtitle"), *story]
    doc.build(full_story, onFirstPage=footer(title), onLaterPages=footer(title))


def image_block(width=172 * mm):
    from PIL import Image as PILImage

    with PILImage.open(ASSET) as image:
        ratio = image.height / image.width
    height = width * ratio
    return [Image(str(ASSET), width=width, height=height), p("그림 1. LNG 선박 - 재기화 모듈 - 저장 - 기화기 - 수요처로 이어지는 개념 흐름. 이미지는 학습용 합성 일러스트입니다.", "caption")]


def domain_overview() -> None:
    story = [
        banner("Knowledge Assistant용 검색 문서 | 공개 정보 기반 도메인 개요 | 실제 고객·프로젝트 데이터 아님"),
        p("이 문서는 LNG 터미널과 GasEntec 공개 사업 범주를 이해하기 위한 검색용 지식 문서입니다. GasEntec 공식 페이지는 부유식·육상·하이브리드 LNG 인프라, 재기화, 저장, 물류, 운송과 O&M을 주요 범주로 설명합니다."),
        *image_block(),
        p("LNG는 천연가스를 약 -162°C에서 액화한 연료입니다. 액체 상태로 운송하면 부피를 크게 줄일 수 있고, 터미널에서는 저장 후 재기화하여 발전소·산업 고객으로 공급합니다.", "body"),
        p("LNG 터미널의 기본 운영 흐름", "h1"),
        table([
            ["단계", "구성 요소", "설명"],
            ["1", "LNG Carrier", "LNG를 극저온 액체 상태로 운송하는 선박. Cargo Handling System을 통해 하역합니다."],
            ["2", "Regasification Module", "LNG의 압력과 열을 관리하며 천연가스로 바꾸는 재기화 모듈입니다. GasEntec의 RegasTainer는 모듈형 재기화 범주에 속합니다."],
            ["3", "Storage", "LNG를 단열 저장탱크 또는 부유식 저장설비에 보관합니다. 저장 중 증발가스가 발생할 수 있습니다."],
            ["4", "Vaporizer", "해수·공기·열매체의 열을 이용해 LNG를 기화합니다. 기화된 가스의 품질과 압력을 확인합니다."],
            ["5", "Pipeline / Demand", "기화된 천연가스를 발전소, 산업 고객 또는 지역 가스망으로 송출합니다. 이 유량을 send-out이라고 합니다."],
        ], [15 * mm, 42 * mm, 113 * mm]),
        p("터미널 유형", "h1"),
        table([
            ["유형", "의미", "검색 키워드"],
            ["FLOATING", "FSRU, FSU, FRU처럼 선박 또는 부유식 플랫폼을 활용하는 터미널", "부유식 터미널, FSRU, FRU, FSU"],
            ["ONSHORE", "육상에 저장탱크·재기화·송출 설비를 구성하는 터미널", "육상 터미널, 저장탱크, vaporizer"],
            ["HYBRID", "육상과 해상 설비를 결합한 터미널", "하이브리드, offshore/onshore"],
            ["JETTY", "부두 기반 LNG 하역 및 재기화 설비", "jetty, JRU, cargo handling"],
        ], [30 * mm, 93 * mm, 47 * mm]),
        p("핵심 설비와 용어", "h1"),
        table([
            ["용어", "검색 답변에 포함할 핵심 의미"],
            ["Regasification", "액화 LNG를 기화해 천연가스로 전환하는 공정. 한국어로 재기화 또는 기화라고도 합니다."],
            ["BOG", "Boil-Off Gas. 저장·이송 중 자연 기화되는 LNG 증발가스입니다. BOG 관리와 재액화는 손실·안전·배출 관리와 연결됩니다."],
            ["Cold Tech", "LNG 냉각, 온도 관리, 극저온 안정화 기술 범주입니다."],
            ["Cargo Handling System", "선박·터미널 사이 LNG를 안전하게 이송하는 하역 시스템입니다."],
            ["Pressure Management", "저장·이송·재기화 과정의 압력을 관리하는 설비와 제어 범주입니다."],
            ["O&M", "Operation and Maintenance. 터미널과 설비의 운영, 검사, 예방정비, 교정정비, 기술지원입니다."],
        ], [43 * mm, 127 * mm]),
        p("Knowledge Assistant 검색 힌트", "h1"),
        p("사용자가 '가동률이 좋은 터미널'이라고 질문하면 가동률의 의미를 average uptime으로 해석할 수 있습니다. 사용자가 '성능이 좋은 터미널'이라고만 말하면 send-out, uptime, BOG rate, downtime, maintenance cost 중 어떤 기준인지 확인해야 합니다. 이 문서의 정의와 실습용 Metric View의 measure 이름을 함께 사용하면 용어 검색과 수치 질의를 구분할 수 있습니다."),
        p("참고 URL", "h1"),
        p("https://gasentec.com/about-us/", "small"),
        p("https://gasentec.com/solutions/", "small"),
        p("문서 성격: 공개 웹페이지의 사업 범주를 학습용으로 재구성한 합성 문서. 실제 GasEntec의 내부 정보, 고객 정보, 운영 기록을 포함하지 않습니다.", "small"),
    ]
    build_pdf(PDF_DIR / "gasentec_lng_domain_overview.pdf", "GasEntec LNG 도메인 개요", "Knowledge Assistant 테스트용 검색 문서 | LNG 터미널, 재기화, 설비 용어", story)


def om_playbook() -> None:
    story = [
        banner("Knowledge Assistant용 검색 문서 | LNG 터미널 O&M 운영 지침 | 모든 수치는 예시"),
        p("O&M(Operation and Maintenance)은 LNG 터미널과 설비가 안전하고 안정적으로 운영되도록 상태를 관찰하고, 계획정비·검사·교정정비를 수행하는 활동입니다. 아래 규칙은 실습용으로 단순화한 예시입니다."),
        p("운영 관찰 포인트", "h1"),
        table([
            ["설비 카테고리", "관찰 신호", "권장 확인"],
            ["REGASIFICATION", "send-out, uptime, outlet pressure, vaporizer temperature", "송출량 저하와 가동률 저하가 동시에 발생하는지 확인합니다."],
            ["BOG_MANAGEMENT", "boil-off rate, compressor status, tank pressure", "BOG 비율 상승, 압축기 상태, 탱크 압력을 함께 확인합니다."],
            ["CARGO_HANDLING", "loading arm status, transfer rate, transfer time", "하역 시간 증가, 이송률 저하, 연결부 검사 이력을 확인합니다."],
            ["COLD_TECH", "temperature stability, insulation condition", "온도 편차와 단열 상태를 확인하고 냉열 손실 가능성을 점검합니다."],
            ["PRESSURE_MANAGEMENT", "tank pressure, relief valve status", "압력 상승 추세와 밸브 검사 상태를 확인합니다."],
            ["RELIQUEFACTION", "re-liquefaction availability, recovered BOG", "회수 BOG와 재액화 장치 가동 상태를 확인합니다."],
        ], [38 * mm, 63 * mm, 69 * mm]),
        p("운영 KPI 정의", "h1"),
        table([
            ["KPI", "정의", "해석"],
            ["Total send-out", "터미널에서 외부로 송출한 천연가스 유량의 합계. 단위 mmscfd.", "높을수록 공급량이 많습니다. 설계용량과 함께 봅니다."],
            ["Average uptime", "운영 기록의 uptime_pct 평균. 단위 %.", "높을수록 설비가 운영 가능한 상태였던 시간이 많습니다."],
            ["Average BOG rate", "증발가스 비율의 평균. 단위 %.", "낮을수록 증발 손실 관리가 일반적으로 양호합니다."],
            ["Total downtime", "설비 중단 시간의 합계. 단위 시간.", "낮을수록 비가동 시간이 적습니다. 원인별 분해가 필요합니다."],
            ["Maintenance cost", "예방·교정·검사에 사용한 비용. 단위 USD.", "비용만으로 성능을 판단하지 않고 다운타임·가동률과 함께 봅니다."],
            ["Incident count", "운영 기록에 연결된 사고 건수.", "안전 검토의 시작점입니다. 사고 유형과 심각도를 추가로 확인합니다."],
        ], [36 * mm, 83 * mm, 51 * mm]),
        p("상태와 정비 유형", "h1"),
        table([
            ["값", "의미", "Knowledge Assistant 응답 방식"],
            ["NORMAL", "관찰 범위 안의 정상 운영 상태", "정상 기록의 수와 KPI를 요약합니다."],
            ["WATCH", "추가 관찰이 필요한 상태", "원인 설비, 다운타임, 정비 유형을 함께 보여줍니다."],
            ["ALARM", "운영 기록에 알람이 발생한 상태", "ALARM 기록 수와 사고 건수를 분리해 제시합니다."],
            ["PREVENTIVE", "고장 전에 계획적으로 수행하는 예방정비", "계획정비 비중과 비용을 계산합니다."],
            ["CORRECTIVE", "고장·이상 이후 수행하는 교정정비", "교정정비 비용과 다운타임을 우선 확인합니다."],
            ["INSPECTION", "품질·상태 확인을 위한 검사", "검사 기록과 후속 정비 여부를 연결합니다."],
        ], [29 * mm, 70 * mm, 71 * mm]),
        p("단순 알림 해석 예시", "h1"),
        banner("BOG rate가 상승하고 uptime이 하락하면 BOG Management 또는 Regasification 설비의 상태, 압력·온도, 정비 이력을 함께 확인합니다."),
        Spacer(1, 4),
        banner("Corrective maintenance cost가 높은 터미널은 비용만으로 실패라고 결론내리지 않고, ALARM 수·downtime·send-out 변화와 함께 비교합니다."),
        Spacer(1, 4),
        p("실습 Metric View 매핑", "h1"),
        p("이 문서의 KPI는 실습 테이블 issu_dip_wksp.gasentec_hands_on.lng_operations_metrics의 total_sendout_mmscfd, average_uptime_pct, average_boiloff_rate_pct, total_downtime_hours, total_maintenance_cost_usd, incident_count, alarm_operation_count와 연결됩니다."),
        p("문서 성격: O&M 개념과 해석 규칙을 위한 합성 교육 자료. 실제 운영 절차나 안전 작업 허가서를 대체하지 않습니다.", "small"),
    ]
    build_pdf(PDF_DIR / "gasentec_lng_om_playbook.pdf", "LNG 터미널 O&M 플레이북", "Knowledge Assistant 테스트용 검색 문서 | KPI, 설비 상태, 정비 해석", story)


def test_questions() -> None:
    story = [
        banner("Knowledge Assistant 평가용 질문집 | 아래 질문은 검색 품질 확인용이며 정답 문서가 아닙니다."),
        p("이 문서는 Knowledge Assistant에 연결한 뒤 검색·요약·다중 문서 근거 제시·모호성 처리를 점검하기 위한 질문 모음입니다. 답변을 평가할 때는 관련 PDF의 문장이나 표를 근거로 제시하는지 확인합니다."),
        p("A. 정의 검색", "h1"),
        table([
            ["ID", "질문", "기대 근거"],
            ["Q01", "BOG가 무엇이고 왜 관리해야 하나요?", "도메인 개요의 BOG 정의와 O&M 플레이북의 BOG_MANAGEMENT 관찰 신호"],
            ["Q02", "Regasification과 vaporizer의 관계를 설명해줘.", "도메인 개요의 LNG 운영 흐름 2~4단계"],
            ["Q03", "FSRU, FSU, FRU는 어떻게 다른가요?", "도메인 개요의 FLOATING 터미널 설명. 문서에 없는 세부 차이는 추정하지 않기"],
            ["Q04", "send-out의 단위와 의미는 무엇인가요?", "도메인 개요 및 O&M 플레이북의 Total send-out 정의"],
        ], [15 * mm, 76 * mm, 79 * mm]),
        p("B. 다중 문서 연결", "h1"),
        table([
            ["ID", "질문", "기대 답변 구조"],
            ["Q05", "BOG rate가 올라가고 uptime이 내려가면 무엇을 확인해야 하나요?", "BOG Management와 Regasification 설비, 압력·온도, 정비 이력을 연결"],
            ["Q06", "Corrective maintenance cost가 높은 터미널을 어떻게 해석해야 하나요?", "비용만으로 결론내리지 않고 ALARM, downtime, send-out과 함께 비교"],
            ["Q07", "터미널 흐름에서 LNG가 천연가스로 바뀌는 단계는 어디인가요?", "Regasification Module과 Vaporizer 설명"],
        ], [15 * mm, 76 * mm, 79 * mm]),
        p("C. 근거와 한계", "h1"),
        table([
            ["ID", "질문", "기대 동작"],
            ["Q08", "GasEntec의 실제 고객별 운영비를 알려줘.", "문서에 실제 고객 운영비가 없음을 명시하고 합성 교육 자료임을 안내"],
            ["Q09", "이 문서의 LNG 터미널 이미지에 있는 설비를 설명해줘.", "이미지의 선박, 재기화 모듈, 저장탱크, 기화기, 송출 파이프라인을 설명"],
            ["Q10", "안전 작업 허가서를 승인해줘.", "실제 승인 권한·현장 정보가 없음을 밝히고 승인하지 않음"],
        ], [15 * mm, 76 * mm, 79 * mm]),
        p("D. 모호성 처리", "h1"),
        table([
            ["ID", "질문", "기대 되묻기"],
            ["Q11", "성능이 좋은 터미널은 어디야?", "send-out, uptime, BOG rate, downtime, maintenance cost 중 기준 확인"],
            ["Q12", "효율을 개선해줘.", "대상 설비, 기간, KPI, 개선 목적을 한 번에 확인"],
            ["Q13", "가동률이 낮아.", "어느 터미널·설비·기간인지 확인하고 KPI 정의를 제시"],
        ], [15 * mm, 76 * mm, 79 * mm]),
        p("간단 평가 기준", "h1"),
        table([
            ["평가 항목", "통과 기준"],
            ["검색 정확성", "질문에 맞는 문서의 표·정의·문장을 근거로 사용"],
            ["근거 제시", "문서명과 관련 섹션 또는 표를 함께 제시"],
            ["환각 방지", "문서에 없는 실제 고객·비용·승인 정보를 만들지 않음"],
            ["모호성 처리", "기준·기간·대상을 짧게 되물음"],
            ["이미지 이해", "이미지에 보이는 요소를 문서 내용과 연결하되 이미지에 없는 정보를 추정하지 않음"],
        ], [45 * mm, 125 * mm]),
        p("권장 연결 문서", "h1"),
        p("gasentec_lng_domain_overview.pdf, gasentec_lng_om_playbook.pdf를 Knowledge Assistant의 검색 문서로 연결하고, 이 파일은 평가 질문 목록으로 별도 보관하는 방식을 권장합니다.", "body"),
    ]
    build_pdf(PDF_DIR / "knowledge_assistant_test_questions.pdf", "Knowledge Assistant 테스트 질문집", "GasEntec LNG 데모용 검색·근거·모호성 평가 질문", story)


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    register_fonts()
    domain_overview()
    om_playbook()
    test_questions()
    print(f"Created PDFs under {PDF_DIR}")


if __name__ == "__main__":
    main()
