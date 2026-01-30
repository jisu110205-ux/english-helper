import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO

# Page Settings
st.set_page_config(page_title="English IPA Master", page_icon="🇺🇸")
st.title("🇺🇸 English Pronunciation Helper")

# --- Sidebar: IPA Guide ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    st.write("Click to hear the sounds:")
    ipa_samples = {
        "Vowels (Short)": {"æ": "apple", "ɛ": "bed", "ɪ": "sit", "ɔ": "hot", "ʊ": "foot", "ʌ": "cup", "ə": "ago"},
        "Vowels (Long)": {"i:": "see", "u:": "blue", "a:": "father", "ɔ:": "door", "ɜ:": "bird"},
        "Diphthongs": {"eɪ": "say", "aɪ": "eye", "ɔɪ": "boy", "aʊ": "now", "oʊ": "go"},
        "Consonants": {"ʃ": "ship", "tʃ": "chair", "dʒ": "jump", "θ": "thin", "ð": "this", "ŋ": "sing"}
    }
    for category, symbols in ipa_samples.items():
        st.subheader(category)
        for symbol, example in symbols.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button(symbol, key=f"btn_{symbol}"):
                    tts_symbol = gTTS(text=example, lang='en')
                    sound_fp = BytesIO()
                    tts_symbol.write_to_fp(sound_fp)
                    st.audio(sound_fp, format='audio/mp3')
            with col2:
                st.write(f"as in **{example}**")

# --- Main Screen: Grouped Layout ---
input_text = st.text_area("Enter English Text:", height=150, placeholder="Enter your text here.")

if st.button("Convert & Speak 🚀"):
    if input_text:
        # 1. 원문 표시 (입력한 그대로)
        st.subheader("Original Text")
        st.write(input_text)
        
        st.write("---") # 구분선
        
        # 2. 발음기호 표시 (원문 전체에 대응하는 발음기호 덩어리)
        st.subheader("IPA Transcription")
        ipa_result = ipa.convert(input_text)
        st.info(ipa_result) # 파란색 박스로 발음기호 덩어리 강조
        
        # 3. 전체 음성 재생
        st.write("---")
        sound_file = BytesIO()
        tts = gTTS(text=input_text, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file)
    else:
        st.warning("Please enter some English text first!")