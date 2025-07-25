import streamlit as st
import random

st.title("✊✋✌️ 가위바위보 게임")
st.write("당신은 어떤 선택을 하시겠습니까?")

choices = ["가위", "바위", "보"]
user_choice = st.radio("당신의 선택:", choices, horizontal=True)

# 점수판 초기화
if 'win' not in st.session_state:
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.draw = 0

if st.button("대결 시작!"):
    computer_choice = random.choice(choices)

    st.write(f"🧍 당신: **{user_choice}**")
    st.write(f"💻 컴퓨터: **{computer_choice}**")

    # 결과 판단
    if user_choice == computer_choice:
        result = "무승부입니다! 🤝"
        st.session_state.draw += 1
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        result = "당신이 이겼습니다! 🎉"
        st.session_state.win += 1
    else:
        result = "당신이 졌습니다... 😢"
        st.session_state.lose += 1

    st.subheader(result)

    # 점수판 출력
    st.markdown("---")
    st.markdown("### 📊 점수판")
    st.write(f"✅ 승: {st.session_state.win}")
    st.write(f"🤝 무: {st.session_state.draw}")
    st.write(f"❌ 패: {st.session_state.lose}")

# 점수 초기화 버튼
if st.button("점수 초기화"):
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.draw = 0
    st.success("점수가 초기화되었습니다!")
