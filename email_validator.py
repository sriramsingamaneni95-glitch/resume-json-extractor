"""Tool: validate/clean an email address (Point 2)."""
import re

EMAIL_RE = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")


def validate_email(email: str) -> tuple[bool, str]:
    if not email:
        return False, ""
    email = email.strip()
    return bool(EMAIL_RE.match(email)), email
