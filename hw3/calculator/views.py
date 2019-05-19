from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# def home_page(request):
#     # render takes: (1) the request,
#     #               (2) the name of the view to generate, and
#     #               (3) a dictionary of name-value pairs of data to be
#     #                   available to the view.
#     return render(request, 'calculator/calculator.html', {})


def calculator(request):
    result = 0
    preValue = 0
    newValue = 0
    preOp = 'plus'
    

    if request.method == 'GET':
        return render(request, 'calculator/calculator.html', {})

    context = {}

    number = ["1","2","3","4","5","6","7","8","9","0"]
    operation = ['plus', 'minus', 'times', 'divide', 'equals']
    print(request.POST)

    if 'display' not in request.POST or 'preOp' not in request.POST or 'preValue' not in request.POST or 'last' not in request.POST or 'newValue' not in request.POST or 'button' not in request.POST:
        context['message'] = 'Error!'
        return render(request, 'calculator/error.html', context)
    if 'button' in request.POST:
        button = request.POST['button']

    try:
        if 'display' in request.POST:
            display = request.POST['display']
            display=int(display)
        if 'preOp' in request.POST:
            preOp = request.POST['preOp']
            if preOp not in ['plus', 'minus', 'times', 'divide', 'equals']:
                context['message'] = 'Error!'
                return render(request, 'calculator/error.html', context)
        if 'preValue' in request.POST:
            preValue = int (request.POST['preValue'])
        if 'last' in request.POST:
            last = request.POST['last']
            if last not in ['operation','last','']:
                context['message'] = 'Error!'
                return render(request, 'calculator/error.html', context)

        if 'newValue' in request.POST:
            newValue = int(request.POST['newValue'])


        if button in number:
            digit = button
            digit = int(digit)
            if digit not in [1,2,3,4,5,6,7,8,9,0]:
                context['message'] = 'Error! button value is not correct.'
                return render(request, 'calculator/error.html', context)
            if preOp == 'equals':
                preOp = 'plus'
                preValue = 0
            newValue = newValue * 10 + int(digit)
            result = newValue
            context['newValue'] =newValue
            context['preOp'] = preOp

        elif button in operation:
            op = button
            if op not in ['plus', 'minus', 'times', 'divide', 'equals']:
                context['message'] = 'Error! button value is not correct.'
                return render(request, 'calculator/error.html', context)
            if last == 'operation':
                context['preOp'] = op
                context['preValue'] = preValue
                context['newValue'] = newValue
                context['result'] = preValue
                context['last'] = 'operation'
                return render(request, 'calculator/calculator.html', context)
            if preOp == 'plus' or preOp == 'equals':
                result = preValue + newValue
            elif (preOp) == 'minus':
                result = preValue - newValue
            elif (preOp) == 'times':
                result = preValue * newValue
            elif (preOp) == 'divide':
                if newValue is 0:
                    context['message'] = 'Error! Can not divided by 0.'
                    return render(request, 'calculator/error.html', context)
                result = int(preValue/newValue)

            context['preOp'] = op
            context['last'] = 'operation'
            preValue = result
            newValue = 0

        else:
            context['message'] = 'Error! Missing parameter.'
            return render(request, 'calculator/error.html', context)

        context['preValue'] = preValue
        context['newValue'] = newValue
        context['result'] = result

        return render(request, 'calculator/calculator.html', context)

    except ValueError:
        context['message'] = 'Error! Invalid value.'
        return render(request, 'calculator/error.html', context)
    except:
        context['message'] = 'Error!'
        return render(request, 'calculator/error.html', context)


