from django.forms import forms
from django.template import Context, Template
from users.forms import UserSignupForm


def test_add_css_template_tag(db):
    form = UserSignupForm(
        data={
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email@mail.com",
            "password1": "password1234",
            "password2": "password1234",
        }
    )
    assert form.is_valid()

    template = Template(
        """{% load add_css %}
    {{ form.first_name|addcss:"border" }}"""
    )
    context = Context({"form": form})
    output = template.render(context)
    assert output is not None
    assert "border" in output
    print(output)
