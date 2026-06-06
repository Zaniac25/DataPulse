import google.generativeai as genai

def configure_gemini(api_key):

    genai.configure(
        api_key=api_key
    )

    return genai.GenerativeModel(
        "gemini-2.5-flash"
    )