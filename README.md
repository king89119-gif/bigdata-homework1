````markdown
# 🎤 면접 데이터 도메인 맞춤형 토크나이저 및 형태소 분석 비교 프로젝트

```text
본 프로젝트는 AI Hub의 '채용면접 인터뷰 데이터'를 활용하여 한국어 구어체 도메인에서의 
Subword Tokenizer(BPE, WordPiece)와 형태소 분석기(Mecab, Okt, Kkma)의 성능을 비교 분석한 연구 과제입니다.
````

🔗 **Data Source:** [AI Hub 채용면접 인터뷰 데이터](https://www.google.com/search?q=https://www.aihub.or.kr/aihubdata/data/view.do%3FdataSetSn%3D71592)

-----

## 📂 프로젝트 구조

```text
.
├── Training/                # AI Hub 원천 JSON 데이터 (실행 전 준비)
├── extracted_results/       # 전처리 및 실험 결과 저장 폴더 (자동 생성)
└── mytest/                  # 실행 소스코드 폴더
    ├── 1.makeData.py          # JSON 데이터 추출 및 직군별 분류
    ├── 2.countData.py         # 학습 데이터 통계 분석
    ├── 3.splitData.py         # 데이터 정제(노이즈 제거) 및 평가셋(1~2KB) 분리
    ├── 4.tokenizer.py         # BPE vs WordPiece 비교 학습 및 성능 평가
    └── 5.morphology.py        # Mecab, Okt, Kkma 형태소 분석기 비교 분석
```

-----

## 🛠️ 설치 및 환경 설정

본 프로젝트는 **Python 3.10** 및 **Java 11+** 환경에서 최적화되었습니다.

```bash
# 1. 필수 라이브러리 설치
pip install tokenizers pandas konlpy mecab-python3

# 2. (macOS 사용자) MeCab 엔진 설치
brew install mecab mecab-ko mecab-ko-dic
```

-----

## 🚀 실행 순서 가이드

> **주의:** 모든 스크립트는 `mytest/` 폴더 내부에서 실행해야 상대 경로 참조가 정상 작동합니다.

### 1\. 데이터 추출 및 통계 확인

원본 JSON에서 Q\&A 텍스트를 추출하고, 학습 데이터가 과제 요건(1MB 이상)을 충족하는지 확인합니다.

```bash
python 1.makeData.py  (데이터 생성을 위한 raw데이터는 github에 올리기 힘들어서 제외)
python 2.countData.py
```

### 2\. 데이터셋 정제 및 분리

단순 절삭이 아닌 **줄 단위 정제**를 통해 구분선(`---`) 등 노이즈를 제거하고, 과제 기준(1\~2KB)에 맞춘 유효 평가셋을 생성합니다.

```bash
python 3.splitData.py
```

### 3\. Subword 토크나이저 성능 평가

**BPE**와 **WordPiece** 알고리즘을 학습 데이터 비율별(10%, 50%, 100%)로 학습하고 추론 속도 및 분절 효율성을 비교합니다.

```bash
python 4.tokenizer.py
```

### 4\. 형태소 분석기 비교 분석

한국어 대표 형태소 분석기 3종을 활용하여 구어체 면접 데이터의 형태소 분절 양상을 분석합니다.

```bash
python 5.morphology.py
```

-----

## 📊 실험 결과 요약

### 1\. Subword Tokenizer (BPE vs WordPiece)

  - **BPE:** 학습량이 늘수록 빈번한 패턴을 거대 토큰으로 병합하여 **추론 효율성**이 극대화됨.
  - **WordPiece:** 사전 고도화에 따른 **확률적 최적 분절 탐색 연산**이 증가하여 속도가 미세하게 저하됨.

### 2\. 형태소 분석기 (Morphology)

  - **Mecab:** C++ 기반의 압도적인 처리 속도와 표준적인 분절 성능 제공.
  - **Okt:** 구어체 및 신조어 처리에 강점이 있으며 가독성 중심의 분절 수행.
  - **Kkma:** 정교한 형태소 분절을 수행하나 연산 시간이 상대적으로 김.

-----

## 📄 최종 산출물 (`extracted_results/`)

  - `train_set.txt` / `evaluation_set.txt`: 정제된 학습/평가 데이터셋
  - `tokenizer_comparison_results.csv`: 토크나이저 성능 수치 리포트
  - `morphology_stats.csv`: 형태소 분석기별 성능 통계
  - `morphology_full_comparison.csv`: 문장별 분석기 분절 결과 상세 비교표
