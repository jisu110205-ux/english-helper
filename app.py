import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64

# 1. 페이지 설정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="wide")

# 오디오 자동 재생을 위한 함수 (하얀 박스 방지)
def autoplay_audio(text):
    tts = gTTS(text=text, lang='en')
    data = BytesIO()
    tts.write_to_fp(data)
    b64 = base64.b64encode(data.getvalue()).decode()
    footer_html = f"""
        <audio autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

st.title("🇺🇸 English Pronunciation Helper")

# --- 사이드바: IPA 가이드 ---
with st.sidebar:
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
                # 버튼 클릭 시 하얀 박스 없이 소리만 재생
                if st.button(symbol, key=f"guide_{symbol}"):
                    autoplay_audio(example)
            with col2:
                st.caption(f"as in **{example}**")

# --- 메인 화면: 글자 기억 기능 ---
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# 입력창 (session_state와 연결되어 글자가 지워지지 않음)
input_text = st.text_area("Enter English Text:", value=st.session_state.text_input, height=150, key="main_input")
st.session_state.text_input = input_text

if st.button("Convert & Speak 🚀"):
    if input_text:
        st.subheader("Original Text")
        st.write(input_text)
        
        st.divider()
        
        st.subheader("IPA Transcription")
        ipa_result = ipa.convert(input_text)
        st.info(ipa_result) # 파란색 박스로 깔끔하게 표시
        
        # 메인 음성 재생
        tts_all = gTTS(text=input_text, lang='en')
        sound_file = BytesIO()
        tts_all.write_to_fp(sound_file)
        st.audio(sound_file)
