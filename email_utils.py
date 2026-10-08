
import smtplib
from email.message import EmailMessage


def send_report_email(
    sender_email,
    app_password,
    recipient_email,
    customer_name,
    report_text,
):
    """
    Email a CompareWise AI report as an attachment.
    This function runs only when called.
    """

    message = EmailMessage()

    message["Subject"] = (
        "Your CompareWise AI Product Comparison"
    )

    message["From"] = sender_email
    message["To"] = recipient_email

    message.set_content(
        f"Hello {customer_name},\n\n"
        "Thank you for using CompareWise AI!\n\n"
        "Your product comparison report is "
        "attached to this email.\n\n"
        "Please verify important information "
        "against the original product labels.\n\n"
        "Happy shopping!\n"
        "CompareWise AI Team"
    )

    # Attach the saved comparison report
    message.add_attachment(
        report_text.encode("utf-8"),
        maintype="text",
        subtype="markdown",
        filename="CompareWise_Comparison_Report.md",
    )

    # Connect securely to Gmail SMTP
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        timeout=20,
    ) as smtp:

        smtp.login(
            sender_email,
            app_password,
        )

        smtp.send_message(message)
