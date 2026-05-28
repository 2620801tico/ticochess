import streamlit as st
import random

# 1. 웹 페이지 기본 구성 설정
st.set_page_config(page_title="체스 기보 암기 훈련기", layout="centered")

# 체스판 좌표 정의 (가로 a~h, 세로 1~8)
cols_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows_numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

# 2. 세션 상태(Session State) 초기화
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'target_coord' not in st.session_state:
    st.session_state.target_coord = ""
if 'prev_coord' not in st.session_state:
    st.session_state.prev_coord = ""
if 'result_msg' not in st.session_state:
    st.session_state.result_msg = "아래 '훈련 시작' 버튼을 누르면 문제가 출제됩니다."
if 'result_type' not in st.session_state:
    st.session_state.result_type = "info"

# 3. 중복 없는 다음 좌표 생성 함수
def generate_next_question():
    while True:
        c = random.choice(cols_letters)
        r = random.choice(rows_numbers)
        new_coord = f"{c}{r}"
        
        if new_coord != st.session_state.prev_coord:
            break
            
    st.session_state.target_coord = new_coord

# --- 메인 UI 레이아웃 ---
st.title("♟️ 체스 기보 암기 훈련기")
st.write("화면에 표시되는 좌표를 체스판의 가로(영어)와 세로(숫자)를 확인하여 클릭하세요.")

# 시작 버튼
if st.button("▶️ 훈련 시작", type="primary", use_container_width=True):
    st.session_state.game_started = True
    st.session_state.prev_coord = ""
    st.session_state.result_msg = "훈련이 시작되었습니다! 목표 좌표를 클릭하세요."
    st.session_state.result_type = "info"
    generate_next_question()
    st.rerun()

st.write("---")

# 목표 좌표 출력 영역
if st.session_state.game_started:
    st.markdown(f"### 🎯 목표 좌표: <span style='color: #FF4B4B; font-size: 38px; font-weight: bold;'>{st.session_state.target_coord}</span>", unsafe_allow_html=True)
else:
    st.markdown("### 🎯 목표 좌표: **대기 중**")

# 피드백 결과 메시지 출력
if st.session_state.result_type == "success":
    st.success(st.session_state.result_msg)
elif st.session_state.result_type == "error":
    st.error(st.session_state.result_msg)
elif st.session_state.result_type == "warning":
    st.warning(st.session_state.result_msg)
else:
    st.info(st.session_state.result_msg)

st.write("---")

# --- 4. 8*8 체스판 및 좌표 표시 구현 ---

# [상단 가로 좌표 기호 (a ~ h)] - 끝에 콜론(:) 추가 완료
top_cols = st.columns([1, 2, 2, 2, 2, 2, 2, 2, 2, 1])
for i, letter in enumerate(cols_letters):
    top_cols[i + 1].markdown(f"<div style='text-align: center; font-weight: bold; color: #888;'>{letter}</div>", unsafe_allow_html=True)

# [본문 체스판 및 세로 좌표]
for r_idx, r_val in enumerate(reversed(rows_numbers)):
    grid_cols = st.columns([1, 2, 2, 2, 2, 2, 2, 2, 2, 1])
    
    # 왼쪽 세로 숫자 표시
    grid_cols[0].markdown(f"<div style='text-align: center; font-weight: bold; line-height: 40px; color: #888;'>{r_val}</div>", unsafe_allow_html=True)
    
    # 중앙 8칸 체스 버튼
    for c_idx, c_val in enumerate(cols_letters):
        coord = f"{c_val}{r_val}"
        tile_emoji = "⬜" if (r_idx + c_idx) % 2 == 0 else "⬛"
        
        if grid_cols[c_idx + 1].button(tile_emoji, key=coord, use_container_width=True):
            if not st.session_state.game_started:
                st.session_state.result_msg = "먼저 '훈련 시작' 버튼을 눌러주세요!"
                st.session_state.result_type = "warning"
                st.rerun()
            
            if coord == st.session_state.target_coord:
                st.session_state.result_msg = f"🎉 성공! 정답은 [{coord}] 이었습니다."
                st.session_state.result_type = "success"
                st.session_state.prev_coord = st.session_state.target_coord
                generate_next_question()
                st.rerun()
            else:
                st.session_state.result_msg = f"❌ 실패! 다시 찾으세요. (방금 클릭한 곳: {coord})"
                st.session_state.result_type = "error"
                st.rerun()

    # 오른쪽 세로 숫자 표시
    grid_cols[9].markdown(f"<div style='text-align: center; font-weight: bold; line-height: 40px; color: #888;'>{r_val}</div>", unsafe_allow_html=True)

# [하단 가로 좌표 기호 (a ~ h)] - 끝에 콜론(:) 추가 완료
bottom_cols = st.columns([1, 2, 2, 2, 2, 2, 2, 2, 2, 1])
for i, letter in enumerate(cols_letters):
    bottom_cols[i + 1].markdown(f"<div style='text-align: center; font-weight: bold; color: #888;'>{letter}</div>", unsafe_allow_html=True)