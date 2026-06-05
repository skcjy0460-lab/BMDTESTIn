# GlucoClaim Studio

제2형 당뇨병 경구용 약제의 병용 급여 조합을 검토하는 Streamlit 심사 보조 앱입니다. 사용자 제공 표의 핵심 매트릭스를 선택 가능한 화면으로 재구성했으며, 선택 제품에 따라 허용 조합은 녹색, 인정되지 않는 조합은 적색으로 표시합니다.

## 기능

- 상단 대형 매트릭스: `MET`, `SU`, `DPP-4i`, `SGLT-2i` 등 경구 성분군 조합표와 선택 조합 색상 표시
- 오른쪽: 제품명 검색 및 선택, 성분·성분군·상한금액 표시, 공식 약가 CSV 교체
- 왼쪽: 선택 조합의 가능/불가 판단, 추가 가능한 성분군과 불가능한 성분군 목록
- AI 전문가 검토: HbA1c, 종전 요법 기간, Metformin 사용 불가 사유를 포함한 규칙형 심사 의견
- 인슐린/GLP-1 병용 검토: 경구제 선택값과 연동하여 Insulin, GLP-1 단일제, Insulin+GLP-1 복합제의 급여 조건 안내

## 실행

상위 폴더에 준비된 가상환경을 사용합니다.

```powershell
cd diabetes_medication_app
..\.venv\Scripts\python.exe -m streamlit run app.py
```

다른 환경에서는 Python 3.10 이상에서 설치합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## 테스트

```powershell
cd diabetes_medication_app
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 약가 데이터

`data/drug_catalog.csv`는 앱 형식과 일부 확인 가능한 제품을 포함한 시작 카탈로그입니다. 상한금액은 변동될 수 있으므로 운영 전에는 적용일 기준의 공식 `약제 급여 목록 및 급여 상한금액표` 데이터를 동일한 CSV 열 형식으로 업로드하거나 파일을 교체해야 합니다.

Streamlit Cloud에서는 `data/drug_catalog.csv` 위치를 권장합니다. 실수로 저장소 최상위에 `drug_catalog.csv`를 올린 경우에도 앱이 자동으로 읽도록 지원합니다. 두 위치 모두에 파일이 없다면 내장된 기본 카탈로그로 실행됩니다.

### 관리자 약가 업데이트

일반 방문자에게는 약가 업데이트 메뉴가 표시되지 않습니다. Streamlit Community Cloud의 앱 설정 `Secrets`에 아래 값을 등록한 뒤, 관리자는 앱 주소 끝에 `?admin=1`을 붙여 접속하고 비밀번호를 입력합니다.

```toml
ADMIN_PASSWORD = "관리자만 아는 비밀번호"
```

예시:

```text
https://앱주소.streamlit.app/?admin=1
```

초기 카탈로그에서 금액을 표시한 제품의 공개 확인 페이지:

- 포시리진정10밀리그램, 334원: https://doccent.com/drugwiki/drug/pheeefiz
- 플로가정5밀리그램, 262원: https://doccent.com/drugwiki/drug/9rnvbp8i
- 위디앙정25밀리그램, 347원: https://doccent.com/drugwiki/drug/hyod7to4

CSV 열:

```text
product_name,ingredient,classes,dose,price_krw,price_as_of,source_note
```

성분군 코드는 `MET`, `SU`, `MEG`, `AGI`, `TZD`, `DPP4`, `SGLT2_DA`, `SGLT2_IP`, `SGLT2_EM`, `SGLT2_ER`, `SGLT2_EN`을 사용합니다.

## 공식 근거

- 보건복지부 고시 제2026-117호(약제), `[일반원칙] 당뇨병용제`, 2026-06-01 시행
  - https://www.hira.or.kr/bbsDummy.do?brdBltNo=12077&brdScnBltNo=4&pageIndex=1&pgmid=HIRAA020002000100

본 앱은 청구 검토를 돕는 도구이며 처방 또는 급여 인정 여부를 확정하지 않습니다. 최신 고시, 제품별 허가사항, 환자 기록 및 적용일 약가파일이 우선합니다.

## 인슐린/GLP-1 모듈 기준

- Insulin과 경구용 당뇨병치료제 병용은 HbA1c 7% 이상인 경우 검토하며, 경구제는 최대 2종까지 인정 범위입니다.
- 선택한 경구 2제 조합이 경구제 병용표에서 인정되지 않는 조합이면 Insulin 병용에서도 불가로 표시합니다.
- Enavogliflozin은 Insulin 주사제와 병용 시 인정하지 않는 것으로 반영했습니다.
- GLP-1 단일제는 MET+SU 병용 후 혈당조절 불충분 및 BMI/Insulin 불가 조건을 확인하도록 안내합니다.
- Insulin glargine+Lixisenatide, Insulin degludec+Liraglutide 복합제는 Metformin 병용 조건을 별도 표시합니다.
