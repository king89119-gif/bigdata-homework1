import os

# 1. 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
base_dir = os.path.join(project_root, 'extracted_results')

source_file = os.path.join(base_dir, 'ict_f_n.txt')
eval_file_path = os.path.join(base_dir, 'evaluation_set.txt')
train_file_path = os.path.join(base_dir, 'train_set.txt')

# 2. 파일 존재 확인 및 읽기
if not os.path.exists(source_file):
    print(f"❌ 에러: 원본 파일을 찾을 수 없습니다. 경로: {source_file}")
else:
    with open(source_file, 'r', encoding='utf-8') as f:
        full_content = f.read()

    # 3. 분리 (700자 = 약 1.5~2KB)
    split_point = 700 
    evaluation_set = full_content[:split_point]
    train_set = full_content[split_point:]

    # 4. 파일 저장
    with open(eval_file_path, 'w', encoding='utf-8') as f:
        f.write(evaluation_set)
    with open(train_file_path, 'w', encoding='utf-8') as f:
        f.write(train_set)

    # 5. 결과 확인
    eval_size = os.path.getsize(eval_file_path) / 1024
    print(f"--- 평가/학습 데이터셋 분리 완료 ---")
    print(f"📍 평가셋: {eval_file_path} ({eval_size:.2f} KB)")
    print(f"📍 학습셋: {train_file_path} ({os.path.getsize(train_file_path) / 1024 / 1024:.2f} MB)")

    if 1.0 <= eval_size <= 2.0:
        print("✅ 성공: 과제 요건(1~2KB) 충족!")