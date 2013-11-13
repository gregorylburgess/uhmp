from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from megawatt.settings import STATIC_URL
from megawatt.models import Card, Player, PointSet
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
def index(request):
   
    places=[0]*10
    places[0]="p1_field"
    places[1]="p2_field"
    places[3]="p1_hand"
    places[4]="p2_hand"
    places[5]="neutral_field"
    cards ={}
    for i in range(0,15):
        name=i
        card = Card()
        card.id = i
        card.name= "card"+ str(i)
        card.field = places[i%6]
        if i%2 ==1:
            card.image = "http://a.dryicons.com/images/icon_sets/colorful_stickers_part_2_icons_set/png/256x256/light_bulb.png"
        else:
            card.image = "http://cdn1.iconfinder.com/data/icons/all_google_icons_symbols_by_carlosjj-du/128/lightbulb-y.png"
        cards[card.id]=card
    icons = {}
    icons["nrg"]="img/nrg.png"
    icons["env"]="img/env.jpg"
    icons["dollar"]="img/dollar.gif"
    icons["user"]="img/user.jpeg"
    
    player1 = Player.objects.filter(id=1)
    player2 = Player.objects.filter(id=2)
    ps1 = PointSet.objects.get(player=player1)
    ps2 = PointSet.objects.get(player=player2)
    
    p1=[]
    p2=[]
    
    p1.append(("nrg", icons["nrg"],ps1.nrg))
    p1.append(("env", icons["env"],ps1.env))
    p1.append(("user", icons["user"],ps1.user))
    p1.append(("dollar", icons["dollar"],ps1.dollar))
    
    p2.append(("nrg", icons["nrg"],ps2.nrg))
    p2.append(("env", icons["env"], ps2.env))
    p2.append(("user", icons["user"], ps2.user))
    p2.append(("icons", icons["dollar"], ps2.dollar))
    
    phases = []
    phases.append(("Upkeep","U", True))
    phases.append(("Bidding","B",False))
    phases.append(("Reveal","R",False))
    phases.append(("Installation","I",False))
    phases.append(("Generation","G",False))
    phases.append(("Reconciliation","R",False))
    
    return render_to_response(
              'index.html',
              {
               'STATIC_URL': STATIC_URL,
               'cards':cards,
               'icons':icons,
               'p1':p1,
               'p2':p2,
               'nrg_goal':"11",
               'phases': phases,
               })
    
@csrf_exempt
def update(request, field, id):
    print str("moved "+str(id) + " to " + str(field))
    return HttpResponse(status=200)
    