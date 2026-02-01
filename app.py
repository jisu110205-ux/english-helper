import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64
import re

# 1. 페이지 설정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="centered")

# 기록 저장소 초기화
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. 소리 재생 함수 (속도 조절 기능 포함!) ---
def autoplay_audio(text, speed=1.0):
    try:
        tts = gTTS(text=text, lang='en')
        data = BytesIO()
        tts.write_to_fp(data)
        b64 = base64.b64encode(data.getvalue()).decode()
        
        # 오디오 태그와 속도 조절 자바스크립트
        audio_html = f"""
            <audio id="myAudio" autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                var audio = document.getElementById("myAudio");
                audio.playbackRate = {speed};
            </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception:
        st.error("소리 재생 중 오류가 발생했습니다.")

# --- 3. UI/디자인 ---
st.title("🇺🇸 English Pronunciation Helper")

# 사이드바 설정 (속도와 히스토리)
with st.sidebar:
    st.header("⚙️ Settings")
    speed_choice = st.select_slider("🔊 재생 속도 설정", options=[0.5, 0.75, 1.0], value=1.0)
    st.caption("0.5 (느림) ~ 1.0 (보통)")
    
    st.markdown("---")
    st.header("🕒 최근 검색 기록")
    for word in st.session_state.history[:5]:
        st.write(f"• {word}")

# 메인 입력창
input_text = st.text_area("영어 단어나 문장을 입력하세요:", placeholder="Example: banana, today, how are you?")

if st.button("Convert & Play 🚀", use_container_width=True):
    if input_text:
        # 히스토리 저장
        if input_text not in st.session_state.history:
            st.session_state.history.insert(0, input_text)
        
        # 4. 발음 기호 변환 로직
        ipa_result = ipa.convert(input_text).replace("*", "")
        formatted_ipa = ipa_result.replace(".", " · ")
        
        # 강세(')가 붙은 부분을 빨간색으로 강조
        formatted_ipa = re.sub(r"'([^ ·\s/]+)", r'<span style="color: #ff4757; font-weight: bold;">\1</span>', formatted_ipa)
        
        # --- 5. 발음 기호 디자인 (카드 스타일) ---
        st.markdown(f"""
            <div style="
                background-color: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                border-left: 10px solid #ff4757;
                margin-top: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <p style="margin:0; font-size: 0.9rem; color: #6c757d;">IPA 발음 기호</p>
                <h2 style="margin: 10px 0; font-family: sans-serif; color: #2d3436;">
                    {formatted_ipa}
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        # 소리 재생 실행
        autoplay_audio(input_text, speed=speed_choice)
    else:
        st.warning("텍스트를 입력해주세요!")
