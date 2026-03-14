# 🎤 면접 데이터 도메인 맞춤형 토크나이저 비교 분석 프로젝트

```text
본 프로젝트는 AI Hub의 '채용면접 인터뷰 데이터'를 활용하여 한국어 구어체 도메인에서의 **BPE**와 **WordPiece** 토크나이저 성능을 비교 분석한 연구 과제입니다.
https://www.aihub.or.kr/aihubdata/data/view.do?srchOptnCnd=OPTNCND001&currMenu=115&topMenu=100&searchKeyword=%EC%B1%84%EC%9A%A9&aihubDataSe=data&dataSetSn=71592
```

## 📂 프로젝트 구조
```text
.
├── Training/                # AI Hub 원천 JSON 데이터 (실행 전 준비)
├── extracted_results/       # 전처리 및 실험 결과 저장 폴더 (자동 생성)
└── mytest/                  # 실행 소스코드 폴더
    ├── 1.makeData.py          # JSON 데이터 추출 및 직군별 분류
    ├── 2.countData.py          # 학습 데이터 통계 분석
    ├── 3.extractValidation.py   # 평가 데이터셋(1~2KB) 분리
    └── 4.tokenizer.py          # 토크나이저 비교 학습 및 평가 실행
```

## 🛠️ 설치 및 환경 설정

본 프로젝트는 **Python 3.10** 환경에서 최적화되었습니다. 실행을 위해 터미널(Terminal)에서 아래 명령어를 입력하여 필수 라이브러리를 설치해 주세요.

```bash
# 필수 라이브러리 설치
pip install tokenizers pandas
```


## 🚀 실행 순서 가이드
필독: 모든 스크립트는 mytest 폴더 내부에서 실행해야 합니다. 프로그램 내부에서 상대 경로를 통해 상위 및 하위 폴더를 참조하기 때문입니다.

1. 데이터 전처리 및 추출
원본 JSON 데이터에서 질문(Q)과 답변(A)을 추출하여 텍스트 파일로 변환합니다.

```Bash
python 1.makeData.py
```

2. 데이터셋 통계 분석
추출된 데이터의 용량과 글자 수를 계산하여 학습 데이터 요건(1MB 이상)을 확인합니다.

```Bash
python 2.countData.py
```

3. 평가 데이터셋 생성
학습 데이터에서 과제 기준(1~2KB)에 맞춘 별도의 평가셋을 분리하여 생성합니다.

```Bash
python 3.extractValidation.py
```

4. 토크나이저 비교 학습 및 평가
BPE와 WordPiece 알고리즘을 비율별(10%, 50%, 100%)로 학습하고 최종 성능 리포트를 출력합니다.

```Bash
python 4.tokenizer.py
```

📄 최종 결과물
```text
실행이 완료되면 extracted_results/ 폴더 내에 다음 파일들이 생성됩니다.

train_set.txt / evaluation_set.txt: 학습 및 평가용 데이터셋

tokenizer_comparison_results.csv: 알고리즘별 성능 비교 수치 리포트
```