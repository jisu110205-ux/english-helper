import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64
import re

# 1. 페이지 설정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="wide")

# 기록 저장소 (없으면 만들기)
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 오디오 재생 함수 (이게 있어야 소리가 납니다) ---
def autoplay_audio(text, speed=1.0):
    try:
        tts = gTTS(text=text, lang='en')
        data = BytesIO()
        tts.write_to_fp(data)
        b64 = base64.b64encode(data.getvalue()).decode()
        
        # HTML5 오디오 태그 + 속도 조절 기능
        # id를 random으로 주거나 고정해서 충돌 방지
        audio_html = f"""
            <audio id="audio_{base64.b64encode(text.encode()).decode()[:10]}" autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <script>
                var audio = document.getElementById("audio_{base64.b64encode(text.encode()).decode()[:10]}");
                audio.playbackRate = {speed};
            </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"오디오 오류: {e}")

# 2. 제목
st.title("🇺🇸 English Pronunciation Helper")

# --- 3. 사이드바 (지수님이 찾으시던 발음기호표 + 버튼 복구!) ---
with st.sidebar:
    st.header("⚙️ 설정")
    # 속도 조절 슬라이더
    speed_choice = st.select_slider("재생 속도", options=[0.5, 0.75, 1.0], value=1.0)
    
    st.markdown("---")
    st.header("📖 IPA Sound Guide")
    
    # 지수님이 원하셨던 발음기호 목록 데이터
    ipa_samples = {
        "Vowels (모음)": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot", "ʌ": "cup", "ə": "ago"},
        "Long & Diphthongs": {"i:": "see", "u:": "blue", "eɪ": "say", "aɪ": "eye", "oʊ": "go"},
        "Consonants (자음)": {"ʃ": "ship", "tʃ": "chair", "θ": "thin", "ð": "this", "ŋ": "sing"}
    }

    # 목록을 화면에 뿌리고, 버튼 누르면 소리 나게 하기
    for category, symbols in ipa_samples.items():
        st.subheader(category)
        for symbol, example in symbols.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                # 버튼을 누르면 해당 단어(example)를 읽어줌
                if st.button(symbol, key=f"btn_{symbol}"):
                    autoplay_audio(example, speed=1.0) # 가이드는 보통 속도로
            with col2:
                st.write(f"as in **{example}**")

# --- 4. 메인 화면 (입력창 + 빨간 강세 기능) ---
input_text = st.text_area("영어 텍스트 입력:", height=100, placeholder="여기에 단어나 문장을 입력하세요 (예: Banana)")

if st.button("Convert & Speak 🚀", type="primary"):
    if input_text:
        # 히스토리 저장
        if input_text not in st.session_state.history:
            st.session_state.history.insert(0, input_text)
            
        st.subheader("Original Text")
        st.write(input_text)
        st.divider()
        
        # 발음 기호 변환 및 디자인
        st.subheader("IPA Transcription")
        
        ipa_result = ipa.convert(input_text).replace("*", "") # 별표 제거
        formatted_ipa = ipa_result.replace(".", " · ")
        
        # ★ 빨간색 강세 마법 (지수님이 원하던 기능)
        formatted_ipa = re.sub(r"'([^ ·\s/]+)", r'<span style="color: #ff4757; font-weight: bold;">\1</span>', formatted_ipa)
        
        # 깔끔하게 출력 (이상한 회색 박스 제거함)
        st.markdown(f'<p style="font-size: 1.5rem;">{formatted_ipa}</p>', unsafe_allow_html=True)
        
        # 메인 입력 텍스트 읽어주기 (설정한 속도로)
        autoplay_audio(input_text, speed=speed_choice)

# --- 5. 히스토리 (사이드바 맨 아래) ---
st.sidebar.markdown("---")
st.sidebar.title("🕒 검색 기록")
if st.session_state.history:
    for item in st.session_state.history[:5]:
        st.sidebar.text(f"• {item}")
