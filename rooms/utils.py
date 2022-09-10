from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
import six



def verify_school_email(email_st):
  if 'mail.utoronto.ca' in email_st:
    return True
  return False


# Credits: https://stackoverflow.com/questions/5226329/enforcing-password-strength-requirements-with-django-contrib-auth-views-password
def validate_password(raw_pw):
  min_length = 7

  # check for password size
  if len(raw_pw) < min_length:
    return False, "Password must be a minimum 7 characters..."

  # check for digit
  if not any(char.isdigit() for char in raw_pw):
    return False, "Password must contain at least 1 digit."

  # check for letter
  if not any(char.isalpha() for char in raw_pw):
    return False, "Password must contain at least 1 letter."
  
  return True, ''



class TokenGenerator(PasswordResetTokenGenerator):
  def _make_hash_value(self, user, timestamp):
    return (
      six.text_type(user.pk) + six.text_type(timestamp) +
      six.text_type(user.is_active)
    )

# account_activation_token = TokenGenerator()



