import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64
import re

# 1. 페이지 설정 (깔끔한 레이아웃)
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="centered")

# 기록 저장용 바구니 (세션 스테이트)
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. 소리 재생 함수 (속도 조절 완벽 지원!) ---
def autoplay_audio(text, speed=1.0):
    try:
        tts = gTTS(text=text, lang='en')
        data = BytesIO()
        tts.write_to_fp(data)
        b64 = base64.b64encode(data.getvalue()).decode()
        
        # HTML5 오디오 태그와 자바스크립트로 재생 속도 제어
        audio_html = f"""
            <audio id="audio_tag" autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                var audio = document.getElementById("audio_tag");
                audio.playbackRate = {speed};
            </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error("소리를 생성하는 중 오류가 발생했습니다.")

# --- 3. 화면 UI 디자인 ---
st.title("🇺🇸 English Pronunciation Helper")
st.markdown("##### 발음 기호를 확인하고 원어민의 음성을 천천히 들어보세요.")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ Settings")
    speed_choice = st.select_slider("🔊 Voice Speed", options=[0.5, 0.75, 1.0], value=1.0)
    st.caption("0.5: 아주 느림 | 1.0: 보통")
    
    st.markdown("---")
    st.header("🕒 History")
    if st.session_state.history:
        for word in st.session_state.history[:8]:
            st.write(f"· {word}")
    else:
        st.write("최근 검색 기록이 없습니다.")

# 메인 입력창
input_text = st.text_area("영어 문장이나 단어를 입력하세요:", placeholder="Example: Banana, Information, How are you?")

if st.button("Convert & Play 🚀", use_container_width=True):
    if input_text:
        # 히스토리 추가
        if input_text not in st.session_state.history:
            st.session_state.history.insert(0, input_text)
        
        st.divider()
        
        # 발음 기호 변환
        ipa_result = ipa.convert(input_text).replace("*", "")
        formatted_ipa = ipa_result.replace(".", " · ")
        
        # 강세 하이라이트 (빨간색)
        formatted_ipa = re.sub(r"'([^ ·\s/]+)", r'<span style="color: #FF4B4B; font-weight: 800;">\1</span>', formatted_ipa)
        
        # --- 4. 텍스트 디자인 (카드 스타일로 고급스럽게!) ---
        st.markdown(f"""
            <div style="
                background-color: #f8f9fa;
                padding: 30px;
                border-radius: 15px;
                border-left: 8px solid #FF4B4B;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
                margin: 20px 0;
            ">
                <p style="color: #6c757d; font-size: 0.9rem; margin-bottom: 5px;">IPA Transcription</p>
                <h2 style="color: #2d3436; font-family: 'Courier New', monospace; letter-spacing: 1px;">
                    {formatted_ipa}
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        # 소리 재생 실행
        autoplay_audio(input_text, speed=speed_choice)
    else:
        st.warning("내용을 입력해주세요!")
