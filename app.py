import streamlit as st
import eng_to_ipa as ipa
from gtts import gTTS
from io import BytesIO

# 페이지 설정
st.set_page_config(page_title="Speaking IPA Converter", page_icon="🗣️")

st.title("🗣️ Speaking IPA Converter")
st.write("Paste text below. I will show IPA symbols line-by-line and read it for you!")

# 입력창
input_text = st.text_area("Enter English Text:", height=150, placeholder="Hello.\nI want to make a program.")

if st.button("Convert & Speak 🚀"):
    if input_text:
        # 1. 텍스트를 줄 단위로 나누기
        lines = input_text.split('\n')
        
        st.subheader("📝 Result:")
        
        # 2. 한 줄씩 처리해서 보여주기 (원문 한 줄, 발음 한 줄)
        for line in lines:
            if line.strip(): # 빈 줄이 아닐 때만 실행
                ipa_line = ipa.convert(line)
                
                # HTML을 사용해 예쁘게 꾸미기 (진하게 / 회색)
                st.markdown(
                    f"""
                    <div style="margin-bottom: 10px; padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
                        <p style="font-size:18px; font-weight:bold; margin:0; color: #000;">{line}</p>
                        <p style="font-size:16px; margin:0; color: #555; font-family: monospace;">{ipa_line}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

        # 3. 음성 만들기 (전체 텍스트 읽기)
        st.subheader("🔊 Audio:")
        with st.spinner("Generating audio..."):
            # 구글 TTS로 음성 파일 생성 (메모리에 저장)
            sound_file = BytesIO()
            tts = gTTS(text=input_text, lang='en')
            tts.write_to_fp(sound_file)
            
            # 플레이어 표시
            st.audio(sound_file)
            
    else:
        st.warning("Please enter some text first.")