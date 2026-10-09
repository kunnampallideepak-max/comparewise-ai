# 🛒 CompareWise AI

### Snap. Compare. Choose Smarter.

**CompareWise AI** is an AI-powered shopping assistant that helps users make more informed purchasing decisions by comparing two products from photographs of their labels.

Built with **Python, Streamlit, and Google Gemini**, the app analyses visible product information, compares products based on personal shopping priorities, and generates a downloadable comparison report.

**🌐 Live Application:** https://comparewise-ai-7zkgzbtv5u47jfsxdktcps.streamlit.app/

**💻 GitHub Repository:** https://github.com/kunnampallideepak-max/comparewise-ai

---

## 🎯 Problem Statement

Consumers often find it difficult to compare products because packaging contains lengthy ingredient lists, nutrition tables, technical details, and warnings.

Manually reading and comparing multiple labels can be time-consuming, especially when shoppers have specific priorities such as lower sugar content, fewer ingredients, or better product suitability.

## 💡 Our Solution

CompareWise AI simplifies product comparisons using AI-powered image understanding.

Users upload photographs of two product labels, select a product category, and enter their shopping priority. Google Gemini analyses the visible information and generates a structured comparison with a recommendation based on that priority.

Users can also ask follow-up questions, download reports, restore previous comparisons, and request a report by email.

## ✨ Key Features

- **Personalised onboarding:** Enter your name and email address.
- **Product categories:** Choose Packaged Food, Personal Care, or Household Products.
- **Shopping priorities:** Specify what matters most, such as less sugar or fewer fragrance ingredients.
- **Dual image upload:** Upload label photographs for Product A and Product B.
- **Gemini Vision analysis:** Extract and interpret information visible in product photographs.
- **Side-by-side comparison:** Compare product details in a structured format.
- **AI-powered recommendation:** Receive a recommendation aligned with your shopping priority.
- **Follow-up AI chatbot:** Ask questions about the generated comparison.
- **Markdown report download:** Save your comparison and any successful follow-up conversation.
- **PDF report download:** Export the comparison as a readable PDF.
- **Restore saved comparisons:** Upload a previously downloaded Markdown report without repeating the Gemini image analysis.
- **Email report delivery:** Send the Markdown comparison report as an attachment to the email address entered during onboarding.
- **Basic usage limits:** Per-session Gemini request limits and basic email-sending limits for demonstration purposes.

## 🛍️ Supported Product Categories

1. Packaged Food
2. Personal Care
3. Household Products

## 🔄 How It Works

1. Open the CompareWise AI web application.
2. Enter your name and email address.
3. Select a product category.
4. Enter your shopping priority.
5. Upload photographs of two product labels.
6. Click **Analyse and Compare Products**.
7. Read the AI-generated comparison and recommendation.
8. Optionally ask follow-up questions.
9. Download the report as Markdown or PDF, or request it by email.

To continue with an earlier comparison, use **Restore a Saved Comparison** and upload a previously downloaded `.md` report.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| Google Gemini API | AI-powered product-label analysis and follow-up questions |
| Google GenAI Python SDK | Gemini API integration |
| ReportLab | PDF report generation |
| Gmail SMTP | Optional email report delivery |
| GitHub | Source code hosting and version control |
| Streamlit Community Cloud | Web application deployment |

## 🚀 Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/kunnampallideepak-max/comparewise-ai.git
cd comparewise-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

On Windows, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Streamlit Secrets

Create `.streamlit/secrets.toml` in the project directory.

Add your Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GEMINI_ENABLED = true

EMAIL_ENABLED = false
```

Email delivery is optional for local development. To enable it, configure `EMAIL_SENDER` and `EMAIL_APP_PASSWORD` with a Gmail account and Google App Password.

**Never commit `.streamlit/secrets.toml`, API keys, or email passwords to GitHub.**

### 5. Start the Application

```bash
streamlit run app.py
```

Open the local address shown in your terminal, usually `http://localhost:8501`.

## 📁 Main Project Files

- `app.py` — Streamlit interface, Gemini integration, chatbot, report generation, and application workflow.
- `prompts.py` — System prompt for AI product analysis.
- `email_utils.py` — Gmail SMTP email delivery.
- `requirements.txt` — Python dependencies.
- `README.md` — Project documentation.

## 🔐 Security and Responsible AI

- Gemini API credentials and email credentials are configured through private Streamlit Secrets.
- The app includes basic limits on AI requests and email sending.
- Email delivery requires user consent.
- AI analysis is based on visible information in the uploaded product-label photographs.
- The app instructs the AI not to invent missing or unreadable product information.

**Important:** Basic session and server-instance limits are not production-grade anti-abuse protection. Public email delivery should use stronger verification and persistent rate limiting for long-term deployment.

## ⚠️ Limitations

- AI may misread blurry, cropped, or low-quality photographs.
- Some label details may be missing or unreadable.
- Recommendations depend on the user's selected priority and the available label information.
- Gemini API availability and usage quotas may affect AI features.
- Restored reports reuse saved analysis rather than re-examining the original photographs.
- Users should verify ingredients, nutrition information, warnings, and other important facts against the original product packaging.

CompareWise AI is an **informational shopping assistant**, not a substitute for professional medical, nutritional, or safety advice.

## ✅ Project Status

**Deployed and functional.**

The following features have been implemented and tested:

- Product-label comparison using Gemini
- AI-generated recommendations
- Follow-up chatbot
- Markdown report downloads
- PDF report downloads
- Saved comparison restoration
- Email report delivery

## 🌐 Try CompareWise AI

**Live Demo:** https://comparewise-ai-7zkgzbtv5u47jfsxdktcps.streamlit.app/

**Source Code:** https://github.com/kunnampallideepak-max/comparewise-ai

---

**CompareWise AI — Snap. Compare. Choose Smarter.**