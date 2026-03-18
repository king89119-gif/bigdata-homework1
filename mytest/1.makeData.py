import sys
import io

# 윈도우 표준 출력을 UTF-8로 강제 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

import os
import json
from collections import Counter

# 1. 경로 설정 (상대 경로)
# 현재 스크립트(1.makeData.py)의 위치: .../mytest/
current_dir = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 위치: .../ (mytest의 상위 폴더)
project_root = os.path.dirname(current_dir)

# 데이터를 배치할 예상 경로 (프로젝트 루트의 Training 폴더)
base_dir = os.path.join(project_root, 'Training')
# 결과물이 저장될 폴더 (프로젝트 루트의 extracted_results 폴더)
output_folder = os.path.join(project_root, 'extracted_results')

# 결과 폴더가 없으면 자동 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"폴더 생성됨: {output_folder}")

def split_extract_by_pattern():
    # 데이터가 없을 경우를 대비한 체크
    if not os.path.exists(base_dir):
        print(f"에러: 데이터를 찾을 수 없습니다. \n확인된 경로: {base_dir}")
        print("가이드: GitHub 저장소 루트에 'Training' 폴더를 만들고 JSON 파일들을 넣어주세요.")
        return

    count = 0
    file_handlers = {}
    patterns_found = []

    print(f"데이터 분석 및 추출 시작: {base_dir}")

    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith('.json'):
                # 1. 파일명 패턴 추출
                parts = filename.replace('.', '_').split('_')
                pattern = "_".join(parts[2:-2])
                
                if not pattern: continue
                patterns_found.append(pattern)
                
                # 2. 파일 핸들러 관리
                if pattern not in file_handlers:
                    target_path = os.path.join(output_folder, f"{pattern}.txt")
                    file_handlers[pattern] = open(target_path, 'w', encoding='utf-8')

                # 3. 데이터 추출 및 쓰기
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        data = json.load(f_in)
                        # JSON 구조에 따라 질문과 답변 추출
                        q = data['dataSet']['question']['raw']['text']
                        a = data['dataSet']['answer']['raw']['text']
                        
                        file_handlers[pattern].write(f"Q: {q}\nA: {a}\n{'-'*30}\n")
                        count += 1
                        
                        if count % 5000 == 0:
                            print(f"⏳ 현재 {count:,}개 파일 처리 중...")
                except Exception as e:
                    continue

    # 모든 핸들러 닫기
    for fh in file_handlers.values():
        fh.close()
    
    # 통계 출력
    stats = Counter(patterns_found)
    print(f"\n" + "="*40)
    print(f"작업 완료!")
    print(f"총 처리 파일: {count:,}개")
    print(f"저장 위치: {output_folder}")
    print("-" * 40)
    print("주요 패턴별 추출 결과:")
    for pat, c in stats.most_common(5):
        print(f" - {pat}.txt: {c}개 문답 저장됨")
    print("="*40)

if __name__ == '__main__':
    split_extract_by_pattern()