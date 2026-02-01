import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64
import re

# 1. 페이지 설정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="wide")

# 기록 바구니 만들기
if 'history' not in st.session_state:
    st.session_state.history = []

# 오디오 재생 함수 (속도 조절 기능 포함!)
def autoplay_audio(text, speed=1.0):
    tts = gTTS(text=text, lang='en')
    data = BytesIO()
    tts.write_to_fp(data)
    b64 = base64.b64encode(data.getvalue()).decode()
    
    # 자바스크립트로 속도 조절 마법 부리기
    footer_html = f"""
        <audio id="myAudio" autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <script>
            var audio = document.getElementById("myAudio");
            audio.playbackRate = {speed};
        </script>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

st.title("🇺🇸 English Pronunciation Helper")

# --- 사이드바 영역 ---
with st.sidebar:
    st.header("⚙️ 설정")
    # 속도 조절 메뉴
    speed_choice = st.select_slider("재생 속도 조절", options=[0.5, 0.75, 1.0], value=1.0)
    
    st.markdown("---")
    st.header("📖 IPA Sound Guide")
    ipa_samples = {
        "Vowels": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot", "ʌ": "cup", "ə": "ago"},
        "Long & Diphthongs": {"i:": "see", "u:": "blue", "eɪ": "say", "aɪ": "eye", "oʊ": "go"},
        "Consonants": {"ʃ": "ship", "tʃ": "chair", "θ": "thin", "ð": "this", "ŋ": "sing"}
    }
    for category, symbols in ipa_samples.items():
        st.subheader(category)
        for symbol, example in symbols.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button(symbol, key=f"guide_{symbol}"):
                    autoplay_audio(example, speed=1.0)
            with col2:
                st.caption(f"as in **{example}**")

# --- 메인 화면 입력창 ---
# 지수님 코드에서 빠졌던 '입력창'을 다시 넣었어요!
input_text = st.text_area("Enter English Text:", placeholder="Type something like 'Information' or 'Banana'")

if st.button("Convert & Speak 🚀"):
    if input_text:
        # 1. 히스토리 저장
        if input_text not in st.session_state.history:
            st.session_state.history.insert(0, input_text)

        st.subheader("Original Text")
        st.write(input_text)
        st.divider()

        # 2. 발음 기호 (디자인 수정)
        st.subheader("IPA Transcription")
        ipa_result = ipa.convert(input_text).replace("*", "")
        formatted_ipa = ipa_result.replace(".", " · ")
        
        # 강세 부분 빨간색 + 굵게
        formatted_ipa = re.sub(r"'([^ ·\s/]+)", r'<span style="color: #ff4757; font-weight: bold;">\1</span>', formatted_ipa)
        
        # 보기 좋은 박스에 넣기
        st.markdown(f'''
            <div style="font-size: 1.3rem; background-color: #f0f2f6; padding: 20px; border-radius: 12px; border-left: 5px solid #ff4757;">
                {formatted_ipa}
            </div>
        ''', unsafe_allow_html=True)

        # 3. 오디오 재생 (고른 속도로)
        autoplay_audio(input_text, speed=speed_choice)

# --- 사이드바 하단: 최근 검색 기록 ---
st.sidebar.markdown("---")
st.sidebar.title("🕒 최근 검색 기록")
for word in st.session_state.history[:5]:
    st.sidebar.write(f"- {word}")
