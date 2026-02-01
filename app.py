import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import base64

# 1. 페이지 설정
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸", layout="wide")

# CSS를 사용하여 버튼 간격과 레이아웃을 강제로 고정
st.markdown("""
    <style>
    .ipa-btn {
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        border-radius: 5px;
        padding: 5px 10px;
        cursor: pointer;
        display: inline-block;
        margin-right: 10px;
        text-align: center;
        min-width: 40px;
    }
    .ipa-row {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

def get_audio_base64(text):
    tts = gTTS(text=text, lang='en')
    data = BytesIO()
    tts.write_to_fp(data)
    return base64.b64encode(data.getvalue()).decode()

st.title("🇺🇸 English Pronunciation Helper")

# --- 데이터 유지 ---
if "input_text" not in st.session_state: st.session_state.input_text = ""
if "ipa_result" not in st.session_state: st.session_state.ipa_result = ""

# --- 사이드바: 틈새 절대 방지 로직 ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    st.write("Click symbol to hear sound:")

    ipa_samples = {
        "Vowels": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot", "ʌ": "cup", "ə": "ago"},
        "Long/Diphthongs": {"i:": "see", "u:": "blue", "eɪ": "say", "aɪ": "eye", "oʊ": "go"},
        "Consonants": {"ʃ": "ship", "tʃ": "chair", "θ": "thin", "ð": "this", "ŋ": "sing"}
    }

    for category, symbols in ipa_samples.items():
        st.markdown(f"#### {category}")
        for symbol, example in symbols.items():
            audio_b64 = get_audio_base64(example)
            
            # HTML과 JavaScript를 사용하여 버튼 클릭 시 페이지 새로고침 없이 소리만 재생
            # 이 방식은 Streamlit의 레이아웃 시스템을 타지 않으므로 틈이 생기지 않습니다.
            button_html = f"""
                <div class="ipa-row">
                    <div class="ipa-btn" onclick="new Audio('data:audio/mp3;base64,{audio_b64}').play()">
                        {symbol}
                    </div>
                    <span style='font-size: 14px;'>as in <b>{example}</b></span>
                </div>
            """
            st.components.v1.html(button_html, height=35)

# --- 메인 화면 ---
user_input = st.text_area("Enter English Text:", value=st.session_state.input_text, height=150)
st.session_state.input_text = user_input

if st.button("Convert & Speak 🚀"):
    if user_input:
        st.session_state.ipa_result = ipa.convert(user_input)

if st.session_state.ipa_result:
    st.subheader("Original Text")
    st.write(st.session_state.input_text)
    st.divider()
    st.subheader("IPA Transcription")
    st.info(st.session_state.ipa_result)
    
    # 메인 음성 플레이어
    snd = BytesIO()
    gTTS(text=st.session_state.input_text, lang='en').write_to_fp(snd)
    st.audio(snd)
