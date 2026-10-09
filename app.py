
import re

import streamlit as st
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT
from email_utils import send_report_email
import logging


# ---------------------------------------
# 1. App settings
# ---------------------------------------

MODEL_NAME = "gemini-3.8-flash"
MAX_IMAGE_SIZE = 10 * 1024 * 1024

st.set_page_config(
    page_title="CompareWise AI",
    page_icon="🛒",
    layout="wide",
)


# ---------------------------------------
# 2. Session state
# ---------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "onboarding"

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


def clear_analysis():
    """Clear the old comparison and chat."""
    st.session_state.analysis_result = None
    st.session_state.chat_messages = []


# ---------------------------------------
# 3. Gemini Vision function
# ---------------------------------------

def compare_with_gemini(
    image_a,
    image_b,
    category,
    priority,
    api_key,
):
    """Send two images to Gemini for comparison."""

    client = genai.Client(api_key=api_key)

    request_text = f"""
    Compare the two photographed products.

    Product category: {category}
    User's shopping priority: {priority}

    Analyse Product A and Product B separately.

    Extract visible facts, compare the products,
    and explain which better matches the priority.

    If information is missing, do not guess.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            request_text,

            "This photograph is Product A:",
            types.Part.from_bytes(
                data=image_a.getvalue(),
                mime_type=image_a.type,
            ),

            "This photograph is Product B:",
            types.Part.from_bytes(
                data=image_b.getvalue(),
                mime_type=image_b.type,
            ),
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
        ),
    )

    return response.text



# ---------------------------------------
# Gemini follow-up chat function
# ---------------------------------------

def ask_followup_with_gemini(
    question,
    previous_messages,
    category,
    priority,
    comparison_report,
    api_key,
):
    """Answer questions using the saved comparison."""

    client = genai.Client(api_key=api_key)

    # Keep only the most recent conversation
    # to avoid sending unnecessary text.
    recent_history = previous_messages[-6:]

    history_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in recent_history
    )

    prompt = f"""
    You are answering a follow-up question
    about a product comparison.

    Product category:
    {category}

    User's shopping priority:
    {priority}

    PREVIOUS COMPARISON REPORT:
    {comparison_report[:12000]}

    RECENT CONVERSATION:
    {history_text}

    USER'S NEW QUESTION:
    {question}

    INSTRUCTIONS:
    - Answer the user's question directly.
    - Use the comparison report as your evidence.
    - Do not invent missing label information.
    - If the report does not contain enough
      information, clearly explain that.
    - Do not claim to have re-examined the
      original photos in this follow-up.
    - Keep your answer clear and helpful.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
        ),
    )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty answer."
        )

    return response.text


# ---------------------------------------
# 4. Application heading
# ---------------------------------------

st.title("🛒 CompareWise AI")
st.caption("Snap. Compare. Choose Smarter.")


# ---------------------------------------
# 5. SCREEN 1: Onboarding
# ---------------------------------------

if st.session_state.page == "onboarding":

    st.divider()

    st.header("👋 Welcome to CompareWise AI")

    st.write(
        "Confused about which product to buy? "
        "Compare products using photographs "
        "of their labels and packaging."
    )

    st.subheader("Let's get started!")

    with st.form("onboarding_form"):

        name = st.text_input(
            "Your Name",
            value=st.session_state.user_name,
            placeholder="Enter your name",
        )

        email = st.text_input(
            "Your Email Address",
            value=st.session_state.user_email,
            placeholder="example@gmail.com",
        )

        submitted = st.form_submit_button(
            "Continue →",
            type="primary",
        )

    if submitted:

        name = name.strip()
        email = email.strip()

        if not name:
            st.warning("Please enter your name.")

        elif not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email,
        ):
            st.warning(
                "Please enter a valid email address."
            )

        else:
            st.session_state.user_name = name
            st.session_state.user_email = email
            st.session_state.page = "comparison"

            st.rerun()

    st.stop()


# ---------------------------------------
# 6. SCREEN 2: Product comparison
# ---------------------------------------

st.divider()

st.success(
    f"Welcome, {st.session_state.user_name}! 👋"
)

if st.button("← Edit My Details"):
    st.session_state.page = "onboarding"
    clear_analysis()
    st.rerun()

st.subheader("🛍️ Select Your Products")

category = st.selectbox(
    "Product Category",
    [
        "Packaged Food",
        "Personal Care",
        "Household Products",
    ],
    on_change=clear_analysis,
)

priority = st.text_input(
    "What matters most to you?",
    placeholder=(
        "Example: Less sugar, fewer fragrance "
        "ingredients, better value"
    ),
    on_change=clear_analysis,
)


# ---------------------------------------
# 7. Upload photographs
# ---------------------------------------

st.subheader("📸 Upload Product Labels")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Product A")

    image_a = st.file_uploader(
        "Upload Product A label",
        type=["jpg", "jpeg", "png", "webp"],
        key="product_a",
        on_change=clear_analysis,
    )

    if image_a is not None:
        st.image(
            image_a,
            caption="Product A",
            use_container_width=True,
        )


with col2:

    st.markdown("### Product B")

    image_b = st.file_uploader(
        "Upload Product B label",
        type=["jpg", "jpeg", "png", "webp"],
        key="product_b",
        on_change=clear_analysis,
    )

    if image_b is not None:
        st.image(
            image_b,
            caption="Product B",
            use_container_width=True,
        )


# ---------------------------------------
# 8. Analyse products with Gemini
# ---------------------------------------

st.divider()

# Gemini stays disabled until final testing
try:
    gemini_enabled = st.secrets.get(
        "GEMINI_ENABLED",
        False,
    )
except FileNotFoundError:
    gemini_enabled = False

if not gemini_enabled:
    st.info(
        "Demo Mode: AI product analysis will "
        "be enabled during final testing."
    )

if st.button(
    "🔍 Analyse and Compare Products",
    type="primary",
    disabled=not gemini_enabled,
):

    if not priority.strip():

        st.warning(
            "Please enter your shopping priority."
        )

    elif image_a is None or image_b is None:

        st.warning(
            "Please upload both product photographs."
        )

    elif (
        image_a.size > MAX_IMAGE_SIZE
        or image_b.size > MAX_IMAGE_SIZE
    ):

        st.warning(
            "Each image must be smaller than 10 MB."
        )

    else:

        # Read the secret API key
        try:
            api_key = st.secrets["GEMINI_API_KEY"]

        except (KeyError, FileNotFoundError):
            st.error(
                "Gemini API key not found. "
                "Check .streamlit/secrets.toml."
            )
            st.stop()

        # Call Gemini
        with st.spinner(
            "Gemini is analysing both product labels..."
        ):

            try:
                result = compare_with_gemini(
                    image_a=image_a,
                    image_b=image_b,
                    category=category,
                    priority=priority,
                    api_key=api_key,
                )

                if result:
                    st.session_state.analysis_result = result
                    st.session_state.chat_messages = []
                else:
                    st.error(
                        "Gemini returned no readable analysis."
                    )

            except Exception as error:
                print(f"Gemini API error details: {error}")
                
                st.error(
                    "Gemini analysis failed. "
                    "Check your API key, model access, "
                    "internet connection, and quota."
                )

                st.caption(
                    f"Error type: {type(error).__name__}"
                )


# ---------------------------------------
# 9. Display Gemini's response
# ---------------------------------------

if st.session_state.analysis_result:

    st.divider()

    st.header("📊 Your Product Comparison")

    st.markdown(
        st.session_state.analysis_result
    )

    st.info(
        "AI can misread small or blurry label text. "
        "Verify important ingredients, quantities, "
        "warnings, and nutrition values on the "
        "original packaging before deciding."
    )

# ---------------------------------------
# 10. Follow-up chat interface
# ---------------------------------------

st.divider()

st.subheader("💬 Ask CompareWise AI")

if st.session_state.analysis_result is None:

    with st.chat_message("assistant"):
        st.write(
            "Hello! 👋 Once your products have "
            "been analysed, you can ask me "
            "follow-up questions about them."
        )

    st.chat_input(
        "Available after your first comparison",
        disabled=True,
    )

else:

    st.caption(
        "Ask questions about your comparison. "
        "Each submitted question makes a new "
        "Gemini API request."
    )

    # Display previous conversation
    for message in st.session_state.chat_messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept a new question
    question = st.chat_input(
        "Ask about ingredients, nutrition, "
        "value, or the recommendation..."
    )

    if question and question.strip():

        question = question.strip()

        previous_messages = (
            st.session_state.chat_messages.copy()
        )

        try:
            api_key = st.secrets["GEMINI_API_KEY"]

            with st.spinner(
                "CompareWise AI is thinking..."
            ):

                answer = ask_followup_with_gemini(
                    question=question,
                    previous_messages=previous_messages,
                    category=category,
                    priority=priority,
                    comparison_report=(
                        st.session_state.analysis_result
                    ),
                    api_key=api_key,
                )

        except Exception as error:
            logging.exception("Gemini follow-up request failed")

            st.error(
                "Could not answer the question. "
                "Check the Gemini configuration "
                "when you are ready to test."
            )

            st.caption(
                f"Error type: {type(error).__name__}"
            )

        else:

            # Save the question and answer
            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            st.rerun()


# ---------------------------------------
# 11. Download comparison report
# ---------------------------------------

st.divider()

st.subheader("📥 Download Your Comparison Report")

st.write(
    "Save your product comparison and "
    "follow-up conversation for later."
)

if st.session_state.analysis_result:

    # Create the report content
    report_parts = [
        "# CompareWise AI",
        "## Product Comparison Report",
        "",
        f"**Customer:** {st.session_state.user_name}",
        f"**Product Category:** {category}",
        f"**Shopping Priority:** {priority}",
        "",
        "---",
        "",
        "## Product Analysis",
        "",
        st.session_state.analysis_result,
        "",
    ]

    # Add follow-up questions if available
    if st.session_state.chat_messages:

        report_parts.extend([
            "---",
            "",
            "## Follow-up Conversation",
            "",
        ])

        for message in st.session_state.chat_messages:

            if message["role"] == "user":
                speaker = "Customer"
            else:
                speaker = "CompareWise AI"

            report_parts.extend([
                f"**{speaker}:**",
                "",
                message["content"],
                "",
            ])

    # Add an important disclaimer
    report_parts.extend([
        "---",
        "",
        "## Important Note",
        "",
        "This report was generated with AI.",
        "AI may misread product photographs.",
        "Verify important facts using the",
        "original product packaging.",
        "",
        "Generated by CompareWise AI.",
    ])

    report_text = "\n".join(report_parts)

    # Download the report
    st.download_button(
        label="⬇️ Download Comparison Report",
        data=report_text.encode("utf-8"),
        file_name="CompareWise_Comparison_Report.md",
        mime="text/markdown",
        type="primary",
    )

    st.caption(
        "The report includes your comparison "
        "and any follow-up questions."
    )

else:

    st.info(
        "Your downloadable report will "
        "appear here after your first "
        "successful product comparison."
    )


# ---------------------------------------
# 12. Email comparison report
# ---------------------------------------

st.divider()

st.subheader("📧 Email Your Comparison Report")

if not st.session_state.analysis_result:

    st.info(
        "Complete a product comparison first. "
        "Then you can receive the report by email."
    )

else:

    recipient_email = (
        st.session_state.user_email.strip()
    )

    st.write(
        f"**Report recipient:** {recipient_email}"
    )

    # Email is disabled by default.
    try:
        email_enabled = st.secrets.get(
            "EMAIL_ENABLED",
            False,
        )
    except FileNotFoundError:
        email_enabled = False

    with st.form("email_report_form"):

        consent = st.checkbox(
            "I want to receive this comparison "
            "report by email."
        )

        send_clicked = st.form_submit_button(
            "📤 Send Report by Email",
            disabled=not email_enabled,
        )

    if not email_enabled:

        st.caption(
            "Email sending is currently disabled. "
            "We will enable it during final testing."
        )

    if send_clicked:

        if not consent:

            st.warning(
                "Please confirm that you want "
                "to receive the email."
            )

        else:

            sender_email = st.secrets.get(
                "EMAIL_SENDER",
                "",
            ).strip()

            app_password = st.secrets.get(
                "EMAIL_APP_PASSWORD",
                "",
            ).replace(" ", "")

            allowed_recipient = st.secrets.get(
                "EMAIL_ALLOWED_RECIPIENT",
                "",
            ).strip()

            # Demo safety restriction:
            # only send to an approved address.
            if (
                not allowed_recipient
                or recipient_email.casefold()
                != allowed_recipient.casefold()
            ):

                st.error(
                    "Demo mode: email can only "
                    "be sent to the approved "
                    "recipient address."
                )

            elif (
                not sender_email
                or not app_password
                or app_password == "ADD_LATER"
            ):

                st.error(
                    "Email credentials have "
                    "not been configured yet."
                )

            else:

                try:

                    with st.spinner(
                        "Sending your report..."
                    ):

                        send_report_email(
                            sender_email=sender_email,
                            app_password=app_password,
                            recipient_email=recipient_email,
                            customer_name=(
                                st.session_state.user_name
                            ),
                            report_text=report_text,
                        )

                    st.success(
                        "Your comparison report "
                        "was sent successfully!"
                    )

                except Exception as error:

                    st.error(
                        "Email sending failed. "
                        "Please check the email "
                        "configuration."
                    )

                    st.caption(
                        "Error type: "
                        f"{type(error).__name__}"
                    )
