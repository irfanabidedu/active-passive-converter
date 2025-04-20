import streamlit as st

try:
    from styleformer import Styleformer
    import torch

    # Load Styleformer model with proper error handling
    @st.cache_resource
    def load_model():
        sf_model = Styleformer(style=2)
        return sf_model

    sf = load_model()

    st.title("Active to Passive Voice Converter")
    st.write("Enter a sentence in active voice:")

    text = st.text_input("Your Sentence")

    if st.button("Convert"):
        if text.strip():
            with st.spinner("Converting..."):
                try:
                    passive = sf.transfer(text)
                    st.success(f"Passive Voice:\n\n{passive}")
                except Exception as e:
                    st.error(f"Model error: {str(e)}")
        else:
            st.warning("Please enter a valid sentence.")

except Exception as main_err:
    st.error(f"App loading failed: {main_err}")
