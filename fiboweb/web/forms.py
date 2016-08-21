"""
fiboweb forms
"""
from django import forms


class FibonacciForm(forms.Form):
    """ FibonacciForm """
    user_input = forms.IntegerField(
        label='Integer Number to calculate',
        label_suffix=': ',
        min_value=0,
    )
