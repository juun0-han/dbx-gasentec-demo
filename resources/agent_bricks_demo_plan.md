# Agent Bricks 데모 구성 계획

## 1. Knowledge Assistant

### 목적

LNG 도메인 정의와 O&M 해석 규칙을 PDF 근거와 함께 답변합니다.

### 검색 소스

```text
output/pdf/gasentec_lng_domain_overview.pdf
output/pdf/gasentec_lng_om_playbook.pdf
```

`output/pdf/knowledge_assistant_test_questions.pdf`는 검색 소스가 아니라 평가 질문 목록으로 분리합니다.

### 시연 질문

```text
BOG가 무엇이고 왜 관리해야 하나요?
Regasification과 vaporizer의 관계를 설명해줘.
BOG rate가 올라가고 uptime이 내려가면 무엇을 확인해야 하나요?
```

## 2. AI Search 용어집

### 소스 테이블

```text
issu_dip_wksp.gasentec_hands_on.gasentec_lng_glossary
```

### Index

```text
issu_dip_wksp.gasentec_hands_on.gasentec_lng_glossary_index
```

### 검색 필드

```text
term
definition
preferred_usage
aliases
example_question
metric_or_field
resolution_rule
search_text
```

### 시연 질문

```text
FSRU가 뭐야?
send-out의 의미를 알려줘.
Preventive maintenance와 Corrective maintenance의 차이는?
```

## 3. Supervisor

### 사용 도구

```text
genie_agent
knowledge_assistant
ai_search
dashboard_builder
clarification
```

### 라우팅 기준

```text
운영 수치·비교·추이·집계 → genie_agent
정의·약어·동의어·용어 → ai_search
PDF 기반 설명·O&M 해석 → knowledge_assistant
Dashboard 생성·수정 → dashboard_builder
기준·기간·대상이 모호함 → clarification
```

### Supervisor prompt

```text
resources/supervisor_prompt.md
```

## 4. 시연 포인트

```text
같은 질문을 Genie Agent와 Knowledge Assistant에 각각 보낸다.
수치 질문은 Metric View 근거를 사용한다.
용어 질문은 glossary 또는 PDF 근거를 사용한다.
모호한 성능 질문은 기준을 되묻는다.
답변에 사용한 route와 근거를 App 화면에 표시한다.
```
