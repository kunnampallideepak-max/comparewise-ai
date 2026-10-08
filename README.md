
# 🛒 CompareWise AI

### Snap. Compare. Choose Smarter.

CompareWise AI is an AI-powered shopping assistant
that helps users compare products by uploading
photographs of their labels.

Built using Python, Streamlit, and Google Gemini Vision.

## The Problem

Product packaging often contains lengthy ingredient
lists, nutrition tables, warnings, and specifications.

Reading and comparing multiple products manually
can be time-consuming.

## Our Solution

CompareWise AI allows users to upload product-label
photographs and receive a comparison based on their
personal shopping priorities.

## Features

- Name and email onboarding
- Product category selection
- Personalised shopping priorities
- Two product-label image uploads
- AI-powered label analysis
- Side-by-side product comparison
- AI follow-up questions
- Downloadable Markdown comparison report
- Optional email report functionality

## Supported Categories

- Packaged Food
- Personal Care
- Household Products

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI Python SDK
- Gmail SMTP (optional)

## Running Locally

1. Clone or download the repository.
2. Create a Python virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Copy `.streamlit/secrets.toml.example`
   to `.streamlit/secrets.toml`.

5. Add your Gemini API key to the private
   `secrets.toml` file.

6. Run:

   streamlit run app.py

## Important Notes

- AI may misread blurry or incomplete labels.
- Missing product information must not be guessed.
- Users should verify important facts against
  the original packaging.
- Email delivery is disabled by default.
- Never commit API keys or passwords to GitHub.

## Project Status

Under development. Final Gemini integration
testing and deployment are pending.
