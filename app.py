import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO
import re

st.set_page_config(page_title="Line-by-Line IPA Converter", page_icon="🗣️")
st.title("🗣️ English & Korean Pronouncer")

# --- 사이드바: 발음 가이드 (기능 유지) ---
with st.sidebar:
    st.header("📖 IPA Sound Guide")
    st.write("Click the buttons to hear the sound!")
    ipa_samples = {
        "æ": ("apple", "애"), "ɛ": ("bed", "에"), "ɪ": ("sit", "이"),
        "ɔ": ("hot", "아/오"), "ʊ": ("foot", "우"), "ʃ": ("ship", "쉬"),
        "θ": ("thin", "번데기"), "ð": ("this", "돼지꼬리")
    }
    for symbol, (example, desc) in ipa_samples.items():
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button(symbol, key=symbol):
                tts_symbol = gTTS(text=example, lang='en')
                sound_fp = BytesIO()
                tts_symbol.write_to_fp(sound_fp)
                st.audio(sound_fp, format='audio/mp3')
        with col2:
            st.write(f"like **{example}** ({desc})")

# --- 메인 화면: 줄바꿈 최적화 ---
input_text = st.text_area("Enter Text (English or Korean):", height=150)

if st.button("Convert & Speak 🚀"):
    if input_text:
        lines = input_text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                if re.search("[가-힣]", line):
                    # 한국어 출력
                    st.markdown(f"🇰🇷 **{line}**")
                else:
                    # 영어: 원문 바로 밑에 발음기호 출력
                    ipa_line = ipa.convert(line)
                    st.markdown(f"🇺🇸 **{line}**") # 원문
                    st.code(ipa_line, language=None) # 바로 밑에 발음기호 (회색 박스로 강조)
                st.write("") # 문장 사이 간격 살짝 띄우기

        # 전체 음성 재생
        sound_file = BytesIO()
        detected_lang = 'ko' if re.search("[가-힣]", input_text) else 'en'
        tts = gTTS(text=input_text, lang=detected_lang)
        tts.write_to_fp(sound_file)
        st.audio(sound_file)