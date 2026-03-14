from django.shortcuts import render

# Create your views here.
def contact(req):
  return render(req, "contact.html", {'hidden_search': True})

def about(req):
  return render(req, 'about.html', {'hidden_search': True})