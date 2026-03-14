import os
import time
import pandas as pd
from tokenizers import Tokenizer, models, trainers, pre_tokenizers

# 1. 경로 설정 (상대 경로 방식)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
base_dir = os.path.join(project_root, 'extracted_results')

train_file = os.path.join(base_dir, 'train_set.txt')
eval_file = os.path.join(base_dir, 'evaluation_set.txt')

def run_tokenizer_assignment():
    # 데이터 존재 여부 확인
    if not os.path.exists(train_file) or not os.path.exists(eval_file):
        print("❌ 에러: 학습 또는 평가 데이터셋이 없습니다. 3번 스크립트를 먼저 실행하세요.")
        return

    # 2. 데이터 불러오기
    with open(train_file, 'r', encoding='utf-8') as f:
        train_data = [line.strip() for line in f if line.strip()]
    
    with open(eval_file, 'r', encoding='utf-8') as f:
        eval_data = [line.strip() for line in f if line.strip()]

    experiment_results = []
    ratios = [0.1, 0.5, 1.0]
    algorithms = ["BPE", "WordPiece"]

    print("🚀 토크나이저 학습 및 평가를 시작합니다...")

    for algo in algorithms:
        for r in ratios:
            num_samples = int(len(train_data) * r)
            train_subset = train_data[:num_samples]
            
            # 토크나이저 설정
            if algo == "BPE":
                tokenizer = Tokenizer(models.BPE(unk_token="[UNK]"))
                trainer = trainers.BpeTrainer(vocab_size=5000, special_tokens=["[UNK]", "[PAD]", "[CLS]", "[SEP]", "[MASK]"])
            else:
                tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
                trainer = trainers.WordPieceTrainer(vocab_size=5000, special_tokens=["[UNK]", "[PAD]", "[CLS]", "[SEP]", "[MASK]"])
            
            tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
            
            # (1) 학습 시간 측정
            start_train = time.time()
            tokenizer.train_from_iterator(train_subset, trainer=trainer)
            train_time = time.time() - start_train
            
            # (2) 속도 및 성능 평가
            start_eval = time.time()
            total_tokens = 0
            for line in eval_data:
                encoded = tokenizer.encode(line)
                total_tokens += len(encoded.ids)
            end_eval = time.time()
            
            eval_speed_ms = (end_eval - start_eval) * 1000 
            avg_tokens = total_tokens / len(eval_data) 
            
            experiment_results.append({
                "Algorithm": algo,
                "Train Size": f"{int(r*100)}%",
                "Train Time (s)": round(train_time, 4),
                "Inference Speed (ms)": round(eval_speed_ms, 4),
                "Avg Tokens/Sentence": round(avg_tokens, 2)
            })
            print(f"✅ 완료: {algo} - {int(r*100)}% 학습")

    # 4. 결과 출력 및 저장
    df = pd.DataFrame(experiment_results)
    print("\n" + "="*60)
    print("      토크나이저 비교 분석 리포트 (통계)")
    print("="*60)
    print(df)
    
    report_path = os.path.join(base_dir, 'tokenizer_comparison_results.csv')
    df.to_csv(report_path, index=False, encoding='utf-8-sig')
    print(f"\n📊 최종 리포트 저장 완료: {report_path}")

if __name__ == "__main__":
    run_tokenizer_assignment()