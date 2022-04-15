from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameConverter:
    regex = r'^[\w.@+-]+'

    def to_python(self, value):
        return value

    def to_url(self, value):  # url reverse 시에 호출
        return value