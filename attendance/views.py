from django.shortcuts import render

# views
def index(request):
    """View function for home page of site."""

    context = {
        'hello_context': "Hello Context!",
    }

    return render(request, 'index.html', context=context)
