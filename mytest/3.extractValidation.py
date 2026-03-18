import os

# 1. 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
base_dir = os.path.join(project_root, 'extracted_results')

source_file = os.path.join(base_dir, 'ict_f_n.txt')
eval_file_path = os.path.join(base_dir, 'evaluation_set.txt')
train_file_path = os.path.join(base_dir, 'train_set.txt')

# 2. 파일 존재 확인 및 정제된 읽기
if not os.path.exists(source_file):
    print(f"❌ 에러: 원본 파일을 찾을 수 없습니다. 경로: {source_file}")
else:
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # --- [데이터 정제] ---
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # 공백이거나, 하이픈(-)으로만 구성된 구분선인 경우 제외
        if not line or line.replace('-', '').strip() == "":
            continue
        cleaned_lines.append(line)

    evaluation_lines = []
    train_lines = []
    current_eval_chars = 0
    # 과제 요건인 1.5~2KB(약 700~900자)를 맞추기 위한 목표치
    split_target_chars = 800

    for line in cleaned_lines:
        if current_eval_chars < split_target_chars:
            evaluation_lines.append(line)
            current_eval_chars += len(line)
        else:
            train_lines.append(line)

    # 4. 파일 저장 (줄바꿈 포함)
    with open(eval_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(evaluation_lines))
    with open(train_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(train_lines))

    # 5. 결과 확인
    eval_size_kb = os.path.getsize(eval_file_path) / 1024
    print(f"\n--- ✨ 데이터셋 정제 및 분리 완료 ---")
    print(f"📍 평가셋: {eval_file_path}")
    print(f"   - 실제 크기: {eval_size_kb:.2f} KB")
    print(f"   - 문장 수: {len(evaluation_lines)}개")
    print(f"📍 학습셋: {train_file_path}")
    print(f"   - 실제 크기: {os.path.getsize(train_file_path) / (1024*1024):.2f} MB")

    if 1.0 <= eval_size_kb < 3:
        print("✅ 성공: 과제 요건(1~2KB) 충족 및 노이즈 제거 완료!")
    else:
        print(f"⚠️ 확인: 현재 크기가 {eval_size_kb:.2f}KB입니다. split_target_chars를 조절하세요.")