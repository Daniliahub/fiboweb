from django.shortcuts import render
from django.http import HttpResponseRedirect

from fiboweb.web.forms import FibonacciForm
from fiboweb.web.utils import NthFibonacci


def fibonacci(request):
    if request.method == 'POST':
        form = FibonacciForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['user_input']
            nth_fibonacci = NthFibonacci(number)()
            ctx = {
                'form': form,
                'status': 'SUCCESS',
                'nfib': nth_fibonacci,
                'number': number,
            }
        else:
            ctx = {'form': form}
    else:
        form = FibonacciForm()
        ctx = {'form': form}
    return render(request, 'fibonacci.html', ctx)
