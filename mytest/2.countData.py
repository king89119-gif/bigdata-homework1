import sys
import io

# 윈도우 표준 출력을 UTF-8로 강제 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# 이후 기존 코드 실행...

import os

# 1. 경로 설정 (상대 경로 방식)
# 현재 스크립트(2.countData.py)의 위치: .../mytest/
current_dir = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 위치: .../ (mytest의 상위 폴더)
project_root = os.path.dirname(current_dir)

# 추출된 결과물이 있는 폴더 경로 (상위 폴더의 extracted_results)
dir_path = os.path.join(project_root, 'extracted_results')

# 분석 대상 파일 리스트
target_files = ['ict_f_e.txt', 'ict_f_n.txt', 'ict_m_e.txt', 'ict_m_n.txt']

print(f"{'파일명':<15} | {'용량':>8} | {'전체 글자수':>12} | {'공백제외 글자수':>12}")
print("-" * 70)

total_size_mb = 0
total_chars = 0
total_no_space = 0

# 데이터 존재 여부 먼저 확인
if not os.path.exists(dir_path):
    print(f"에러: 폴더를 찾을 수 없습니다. 경로: {dir_path}")
    print("가이드: 1.makeData.py를 먼저 실행하여 데이터를 추출하세요.")
else:
    for file_name in target_files:
        full_path = os.path.join(dir_path, file_name)
        
        if os.path.exists(full_path):
            # 1. 파일 크기 계산
            size_mb = os.path.getsize(full_path) / (1024 * 1024)
            
            # 2. 글자수 계산
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                chars = len(content)
                # 공백, 줄바꿈 제거 후 글자수 계산
                no_space = len(content.replace(" ", "").replace("\n", "").replace("\r", ""))
                
            print(f"{file_name:<15} | {size_mb:>7.2f}MB | {chars:>11,}자 | {no_space:>13,}자")
            
            total_size_mb += size_mb
            total_chars += chars
            total_no_space += no_space
        else:
            print(f"{file_name:<15} | {'파일 없음':^51}")

    print("-" * 70)
    print(f"{'전체 합계':<15} | {total_size_mb:>7.2f}MB | {total_chars:>11,}자 | {total_no_space:>13,}자")

    # 과제 요건 확인용 안내 메시지
    print("\n[과제 요건 체크]")
    if total_size_mb >= 1.0:
        print(f"학습 데이터셋 크기: {total_size_mb:.2f}MB (1MB 이상 요건 충족)")
    else:
        print(f"학습 데이터셋 크기 부족: {total_size_mb:.2f}MB (추가 데이터 확보 필요)")