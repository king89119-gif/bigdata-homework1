import os
import sys
import time
import pandas as pd

import os
import sys
import time
import pandas as pd

# 1. KoNLPy 로드 (Mecab 포함)
from konlpy.tag import Okt, Kkma, Mecab

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
base_dir = os.path.join(project_root, 'extracted_results')
eval_file = os.path.join(base_dir, 'evaluation_set.txt')

def run_final_eval():
    if not os.path.exists(eval_file):
        print(f"❌ 에러: {eval_file} 파일이 없습니다.")
        return

    # Evaluation.txt 파일의 모든 문장 읽기
    with open(eval_file, 'r', encoding='utf-8') as f:
        sentences = [line.strip() for line in f if line.strip()]

    # 분석기 리스트 (Mecab, Okt, Kkma)
    taggers = {
        'Mecab': Mecab(), 
        'Okt': Okt(), 
        'Kkma': Kkma()
    }

    stats = []
    comparison_details = []

    print(f"🚀 [분석 시작] Mecab, Okt, Kkma 비교 평가를 진행합니다. (대상: {len(sentences)}개 문장)")

    for name, tagger in taggers.items():
        start = time.time()
        total_tokens = 0
        
        # 전체 성능 측정 및 상세 결과 수집
        for idx, sent in enumerate(sentences):
            morphs = tagger.morphs(sent)
            total_tokens += len(morphs)
            
            # 첫 실행 시에만 상세 결과 리스트 초기화 (문장별 비교용)
            if name == 'Mecab':
                comparison_details.append({'Original': sent})
            
            comparison_details[idx][f'{name}_Result'] = " / ".join(morphs)
            
        duration = (time.time() - start) * 1000
        
        stats.append({
            "Algorithm": name,
            "Total_Tokens": total_tokens,
            "Avg_Tokens": round(total_tokens / len(sentences), 2),
            "Speed_ms": round(duration, 2)
        })
        print(f"✅ {name:6} 분석 완료!")

    # 데이터프레임 생성
    df_stats = pd.DataFrame(stats)
    df_details = pd.DataFrame(comparison_details)

    # --- 터미널 출력 개선 (문장별 상세 비교를 세로로 출력) ---
    print("\n" + "="*80)
    print("📊 [성능 통계 결과]")
    print("-" * 80)
    print(df_stats)
    
    print("\n🔍 [상세 분절 양상 비교 (상위 3개 문장)]")
    print("-" * 80)
    
    # 상위 3개 문장만 추출해서 보기 좋게 출력
    for idx, row in df_details.head(3).iterrows():
        print(f"[{idx+1}] 원문: {row['Original']}")
        if 'Mecab_Result' in row:
            print(f"   - Mecab: {row['Mecab_Result']}")
        print(f"   - Okt:   {row['Okt_Result']}")
        print(f"   - Kkma:  {row['Kkma_Result']}")
        print("-" * 80)
    
    print(f"💾 상세 전체 결과는 CSV 파일을 확인하세요: {base_dir}")
    print("="*80)

    # 결과 저장
    df_stats.to_csv(os.path.join(base_dir, 'morphology_stats.csv'), index=False, encoding='utf-8-sig')
    df_details.to_csv(os.path.join(base_dir, 'morphology_full_comparison.csv'), index=False, encoding='utf-8-sig')
    
    print(f"💾 결과 저장 완료: {base_dir} 폴더를 확인하세요.")

if __name__ == "__main__":
    run_final_eval()