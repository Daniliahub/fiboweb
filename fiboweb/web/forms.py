"""
fiboweb forms
"""
from django import forms


class FibonacciForm(forms.Form):
    """ FibonacciForm """
    user_input = forms.IntegerField(
        label='Please enter n to calculate the nth fibonacci number',
        label_suffix=': ',
        min_value=0,
    )
