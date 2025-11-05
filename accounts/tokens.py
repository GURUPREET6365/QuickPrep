# accounts/tokens.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Include user's primary key, password, and is_active status in the token
        # Token becomes invalid if user's password or is_active status changes
        return (
            str(user.pk) + user.password + 
            str(user.is_active) + str(timestamp)
        )

# Create an instance to use throughout the app
email_verification_token = EmailVerificationTokenGenerator()
