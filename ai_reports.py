import google.generativeai as genai

def configure_gemini(api_key):

    genai.configure(
        api_key=api_key
    )

    return genai.GenerativeModel(
        "gemini-2.5-flash"
    )

def generate_ai_eda_report(
        profile,
        insights,
        advanced_insights,
        api_key
    ):

    model = configure_gemini(
        api_key
    )

    prompt = f"""
        You are a Senior Data Analyst.

        Generate a professional EDA report.

        Dataset Profile:
        {profile}

        Basic Insights:
        {insights}

        Advanced Insights:
        {advanced_insights}

        Structure the report as:

        1. Dataset Overview
        2. Data Quality Assessment
        3. Missing Value Analysis
        4. Outlier Analysis
        5. Correlation Analysis
        6. Key Risks
        7. Recommendations

        Use professional but easy-to-understand language.
        """

    response = model.generate_content(
        prompt
    )

    return response.text

def generate_executive_summary(
        profile,
        insights,
        advanced_insights,
        api_key
    ):

    model = configure_gemini(
        api_key
    )

    prompt = f"""
        You are a Senior Business Analyst.

        Generate an Executive Summary.

        Dataset Profile:
        {profile}

        Insights:
        {insights}

        Advanced Insights:
        {advanced_insights}

        Provide:

        1. Overall Dataset Quality
        2. Key Findings
        3. Major Risks
        4. Recommended Actions
        5. Final Verdict

        Keep the report concise and business-friendly.

        Maximum 300 words.
        """

    response = model.generate_content(
        prompt
    )

    return response.text