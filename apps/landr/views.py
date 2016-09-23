from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Poke

# Create your views here.


def index(request):
    return render(request, "landr/index.html")


def register(request):
    if request.method=="POST":
        reg_data = Register.objects.new_reg(request.POST)
        if reg_data['created']:
            messages.success(request, "{} successfully registered".format(reg_data['new_user'].name))
        else:
            for error in reg_data['errors']:
                messages.error(request, error)
    return redirect('landr:index')


def login(request):
    if request.method == "POST":
        user = Register.objects.login(request.POST)
        if user['log_in']:
            request.session['user_id'] = user['user'].id
            return redirect('landr:success')
        else:
            for error in user['errors']:
                messages.error(request, error)
            return redirect('landr:index')

def success(request):
    if "user_id" not in request.session:
        return redirect('index')
    this_user = request.session['user_id']
    context = {
    # "my_pokes": Poke.objects.filter(pokes__id=this_user).count(),
    "other_users": Register.objects.exclude(id=this_user),
    "this_user": Register.objects.get(id=this_user),
    }
    # print(context.my_pokes)
    return render(request, "landr/pokes.html", context)


def poke(request, id):
    if request.method == "POST":
        pokee = Register.objects.get(id=id)
        poker = Register.objects.get(id=request.session['user_id'])
        Poke.objects.create(poked=pokee, poker=poker)
    return redirect('landr:success')


def logout(request):
    request.session.clear()
    return redirect("landr:index")
