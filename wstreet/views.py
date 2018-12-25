from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.db import IntegrityError


def returnDict(request):
    p = Profile.objects.all().order_by('-cash')
    profile = Profile.objects.get(user=request.user)
    cnt = 1
    username = request.user.username
    money = profile.cash
    ns = profile.noShares
    liveT = SU.objects.get(pk=1)
    sellCompanies = UserTable.objects.filter(profile=profile)

    for i in p:
        i.rank = cnt
        cnt += 1
        i.save()
    context = {
        'lb': p,
        'username': username,
        'money': money,
        'ns': ns,
        "company": Company.objects.all(),
        "userTable": UserTable.objects.filter(profile=profile),
        "UserHistory": UserHistory.objects.filter(profile=profile).order_by("-pk"),
        "news": News.objects.all().order_by("-pk"),
        "SellCompany": sellCompanies,
        'LiveText':liveT.LiveText,


    }
    return context


def mainpage(request):
    context = {}
    z = dict(context, **returnDict(request))
    return render(request, "index.html", z)


def Index(request):
    # return mainpage(request, {})
    # return render(request, "index.html")
    return render(request, "login.html")


def getlogin(request):
    uname = request.POST["uname"]
    passwd = request.POST["passwd"]
    user = authenticate(username=uname, password=passwd)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("index/")
    else:
        return render(request, "login.html", {"error_message": "Invalid Username or Password"})
    return HttpResponseRedirect("index")


def logoff(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'login.html')


class Register(View):
    template = 'register.html'

    def get(self, request):
        return render(request, self.template, {})

    def post(self, request):
        try:
            if(str(request.POST["key"])=="kc2334"):
                user = User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
                user.save()
                p = Profile.objects.create(user=user)
                p.save()
                UserTable.objects.create(profile=p)
                return render(request, self.template, {"reg_message": "Registered"})
            else:
                return render(request, self.template, {"error_message": "Could not register"})
        except IntegrityError:
            return render(request, self.template, {"error_message": "Could not register"})


def bid(request):
    spread = SU.objects.get(pk=1)
    spr = spread.Spread

    profile = Profile.objects.get(user=request.user)
    data_set = request.POST
    curr_obj = request.user.userprofile
    userTable = UserTable.objects.filter(profile=curr_obj)
    ns = curr_obj.noShares
    money = curr_obj.cash
    b = Company.objects.get(name=data_set["company"])
    if data_set:
        c = Company.objects.get(name=data_set["company"])
        if ((int(data_set["Price"]) <= 1.10 * c.sharePrice) and (int(data_set["Price"]) >= 0.9 * c.sharePrice) and (
                int(data_set["noShares"]) > 0)and (int(data_set["noShares"]) <=200) and b.remainingShares>0):
            print("Valid")
        else:
            print("invalid")
            context = {'error_message': "Please place a valid bid!", }
            z = dict(context, **returnDict(request))
            return render(request, "index.html", z)

        if c.sixtyFlag:
            b = BuyTable.objects.create(profile=profile, company=Company.objects.get(name=data_set["company"]),
                                        bidPrice=data_set["Price"], bidShares=data_set["noShares"])
            b.save()

            buy_list = BuyTable.objects.filter(company=Company.objects.get(name=data_set["company"])).order_by('-bidPrice')
            sell_list = SellTable.objects.filter(company=Company.objects.get(name=data_set["company"])).order_by(
                'sellPrice')

            if (buy_list and sell_list):
                max_bid = buy_list[0].bidPrice
                max_index = buy_list[0].pk
                min_bid = sell_list[0].sellPrice
                min_index = sell_list[0].pk

                p2 = Profile.objects.get(user=sell_list[0].profile.user)
                p1 = Profile.objects.get(user=buy_list[0].profile.user)

                if max_bid >= min_bid:
                    if buy_list[0].bidShares == sell_list[0].sellShares:
                        print("bought1")

                        spr = spr + ((max_bid - min_bid)*buy_list[0].bidShares)
                        spread.save()
                        buy = BuyTable.objects.get(pk=max_index)

                        thisComp = Company.objects.get(name=buy.company)
                        thisComp.sharePrice = buy.bidPrice
                        thisComp.save()

                        p1.cash = p1.cash - (int(buy.bidPrice)*int(buy.bidShares)*1.05)
                        p1.noShares = p1.noShares + buy_list[0].bidShares

                        p2.cash = p2.cash + (int(buy.bidPrice) * int(buy.bidShares) * 0.95)
                        p2.noShares = p2.noShares - buy_list[0].bidShares



                        p1.save()
                        p2.save()

                        BuyTable.objects.get(pk=max_index).delete()
                        SellTable.objects.get(pk=min_index).delete()

                        u = UserTable.objects.filter(profile=profile)  # ,company=companyName)
                        flagjoin = 0
                        if u:
                            for i in u:
                                print(data_set["company"])
                                print(i.company)
                                if (i.company.name == buy.company.name):
                                    u1 = UserTable.objects.get(profile=profile, company=i.company)
                                    u1.noShares = u1.noShares + int(buy.bidShares)

                                    u1.save()
                                    flagjoin = 1
                                    break

                            if (flagjoin == 0):
                                UserTable.objects.create(profile=profile,
                                                         company=Company.objects.get(name=buy.company),
                                                         noShares=buy.bidShares, pricesShare=buy.bidPrice)


                        else:
                            UserTable.objects.create(profile=profile,
                                                     company=Company.objects.get(name=buy.company),
                                                     noShares=buy.bidShares, pricesShare=buy.bidPrice)

                        u = UserTable.objects.filter(profile=profile)  # ,company=companyName)
                        flagjoin = 0
                        if u:
                            for i in u:
                                print(data_set["company"])
                                print(i.company)
                                if (i.company.name == buy.company.name):
                                    u1 = UserTable.objects.get(profile=profile, company=i.company)
                                    u1.noShares = u1.noShares + int(buy.bidShares)

                                    u1.save()
                                    flagjoin = 1
                                    break

                            if (flagjoin == 0):
                                UserTable.objects.create(profile=profile,
                                                         company=Company.objects.get(name=buy.company),
                                                         noShares=buy.bidShares, pricesShare=buy.bidPrice)


                        else:
                            UserTable.objects.create(profile=profile,
                                                     company=Company.objects.get(name=buy.company),
                                                     noShares=buy.bidShares, pricesShare=buy.bidPrice)

                        u = UserTable.objects.filter(profile=profile)  # ,company=companyName)
                        flagjoin = 0
                        if u:
                            for i in u:
                                print(data_set["company"])
                                print(i.company)
                                if (i.company.name == buy.company.name):
                                    u1 = UserTable.objects.get(profile=profile, company=i.company)
                                    u1.noShares = u1.noShares + int(buy.bidShares)

                                    u1.save()
                                    flagjoin = 1
                                    break

                            if (flagjoin == 0):
                                UserTable.objects.create(profile=profile,
                                                         company=Company.objects.get(name=buy.company),
                                                         noShares=buy.bidShares, pricesShare=buy.bidPrice)


                        else:
                            UserTable.objects.create(profile=profile,
                                                     company=Company.objects.get(name=buy.company),
                                                     noShares=buy.bidShares, pricesShare=buy.bidPrice)





                    elif buy_list[0].bidShares >= sell_list[0].sellShares:
                        print("bought2")

                        spr = spr + ((max_bid - min_bid) * sell_list[0].sellShares)
                        spread.save()
                        buy = BuyTable.objects.get(pk=max_index)
                        sell = SellTable.objects.get(pk=min_index)
                        buy.bidShares = buy.bidShares - sell_list[0].sellShares
                        buy.save()

                        thisComp = Company.objects.get(name=buy.company)
                        thisComp.sharePrice = buy.bidPrice
                        thisComp.save()




                        p1.cash = p1.cash - (int(buy.bidPrice) * int(sell.sellShares) * 1.05)
                        p1.noShares = p1.noShares + sell_list[0].sellShares

                        p2.cash = p2.cash + (int(buy.bidPrice) * int(sell.sellShares) * 0.95)
                        p2.noShares = p2.noShares - sell_list[0].sellShares

                        p1.save()
                        p2.save()


                        SellTable.objects.get(pk=min_index).delete()

                        u = UserTable.objects.filter(profile=profile)  # ,company=companyName)
                        flagjoin = 0
                        if u:
                            for i in u:
                                if (i.company.name == buy.company.name):
                                    u1 = UserTable.objects.get(profile=profile, company=i.company)
                                    u1.noShares = u1.noShares + int(buy.bidShares)
                                    u1.save()
                                    flagjoin = 1
                                    break

                            if (flagjoin == 0):
                                UserTable.objects.create(profile=profile,
                                                         company=Company.objects.get(name=buy.company),
                                                         noShares=buy.bidShares, pricesShare=buy.bidPrice)

                        else:
                            UserTable.objects.create(profile=profile,
                                                     company=Company.objects.get(name=buy.company),
                                                     noShares=buy.bidShares, pricesShare=buy.bidPrice)

                    elif buy_list[0].bidShares <= sell_list[0].sellShares:
                        print("bought3")

                        spr = spr + ((max_bid - min_bid) * buy_list[0].bidShares)
                        spread.save()
                        s = SellTable.objects.get(pk=min_index)
                        s.sellShares = s.sellShares - buy_list[0].bidShares
                        s.save()
                        buy = BuyTable.objects.get(pk=max_index)

                        thisComp = Company.objects.get(name=buy.company)
                        thisComp.sharePrice = buy.bidPrice
                        thisComp.save()


                        p1.cash = p1.cash - (int(buy.bidPrice) * int(buy.bidShares) * 1.05)
                        p1.noShares = p1.noShares + buy_list[0].bidShares

                        p2.cash = p2.cash + (int(buy.bidPrice) * int(buy.bidShares) * 0.95)
                        p2.noShares = p2.noShares - buy_list[0].bidShares

                        p1.save()
                        p2.save()

                        BuyTable.objects.get(pk=max_index).delete()

                        u = UserTable.objects.filter(profile=profile)  # ,company=companyName)
                        flagjoin = 0
                        if u:
                            for i in u:
                                if (i.company.name == buy.company.name):
                                    u1 = UserTable.objects.get(profile=profile, company=i.company)
                                    u1.noShares = u1.noShares + int(buy.bidShares)
                                    u1.save()
                                    flagjoin = 1
                                    break

                            if (flagjoin == 0):
                                UserTable.objects.create(profile=profile,
                                                         company=Company.objects.get(name=buy.company),
                                                         noShares=buy.bidShares, pricesShare=buy.bidPrice)

                        else:
                            UserTable.objects.create(profile=profile,
                                                     company=Company.objects.get(name=buy.company),
                                                     noShares=buy.bidShares, pricesShare=buy.bidPrice)
            profile.save()

        else:
            u = UserTable.objects.filter(profile=profile)  # ,company=companyName)
            flagjoin = 0
            profile.cash = profile.cash - (int(data_set["Price"]) * int(data_set["noShares"]) * 1.05)
            profile.noShares = profile.noShares + int(data_set["noShares"])
            b = Company.objects.get(name=data_set["company"])
            if u:
                for i in u:
                    if (i.company.name == b.name):
                        u1 = UserTable.objects.get(profile=profile, company=i.company)
                        u1.noShares = u1.noShares + int(data_set["noShares"])
                        u1.save()
                        flagjoin = 1
                        break

                if (flagjoin == 0):
                    UserTable.objects.create(profile=profile,
                                             company=Company.objects.get(name=data_set["company"]),
                                             noShares=data_set["noShares"], pricesShare=data_set["Price"])
                    profile.noOfCompanies = profile.noOfCompanies + 1

            else:
                UserTable.objects.create(profile=profile,
                                         company=Company.objects.get(name=data_set["company"]),
                                         noShares=data_set["noShares"], pricesShare=data_set["Price"])
                profile.noOfCompanies = profile.noOfCompanies + 1

            profile.save()

            b.remainingShares = b.remainingShares - int(data_set["noShares"])

            if (b.remainingShares <= 0.6 * b.NumberOfshares):
                b.sixtyFlag = True

            b.save()

        UserHistory.objects.create(profile=profile,
                                   company=Company.objects.get(name=data_set["company"]),
                                   noShares=data_set["noShares"], pricesShare=data_set["Price"], buysell=1,
                                   total=(int(data_set["Price"])*int(data_set["noShares"])*1.05))

        context = {}
        z = dict(context, **returnDict(request))
        return render(request, "index.html", z)
    #return render(request, 'index.html', {'username': request.user.username, 'userTable': userTable, 'ns': ns, 'money': money, "news": News.objects.all().order_by("-pk")})
    context = {}
    z = dict(context, **returnDict(request))
    return render(request, "index.html", z)

def sell(request):

    spread = SU.objects.get(pk=1)
    spr = spread.Spread

    profile = Profile.objects.get(user=request.user)
    data_set = request.POST
    c = Company.objects.get(name=data_set["company"])
    mycompanies = UserTable.objects.filter(profile=profile)
    company = mycompanies
    v = UserTable.objects.get(profile=profile, company=c)
    if ((int(data_set["Price"]) <= 1.10 * c.sharePrice) and (int(data_set["Price"]) >= 0.9 * c.sharePrice) and (
            int(data_set["noShares"]) > 0) and (int(data_set["noShares"]) <= v.noShares)):
        print("Valid")
    else:
        context = {'error_message': "Please place a valid bid!", }
        z = dict(context, **returnDict(request))
        return render(request, "index.html", z)

    profile.noShares = profile.noShares - int(data_set["noShares"])
    #profile.cash = profile.cash + (int(data_set["noShares"]) * int(data_set["Price"]))

    p = UserTable.objects.get(profile=profile, company=Company.objects.get(name=data_set["company"]))
    p.noShares = p.noShares - int(data_set["noShares"])
    if p.noShares == 0:
        p.delete()
    p.save()

    b = SellTable.objects.create(profile=profile, company=Company.objects.get(name=data_set["company"]),
                                 sellPrice=data_set["Price"], sellShares=data_set["noShares"])
    b.save()

    profile.save()

    buy_list = BuyTable.objects.filter(company=Company.objects.get(name=data_set["company"])).order_by('-bidPrice')
    sell_list = SellTable.objects.filter(company=Company.objects.get(name=data_set["company"])).order_by('sellPrice')

    if (buy_list and sell_list):

        max_bid = buy_list[0].bidPrice
        max_index = buy_list[0].pk
        min_bid = sell_list[0].sellPrice
        min_index = sell_list[0].pk

        p2 = Profile.objects.get(user=sell_list[0].profile.user)
        p1 = Profile.objects.get(user=buy_list[0].profile.user)

        if max_bid >= min_bid:
            if buy_list[0].bidShares == sell_list[0].sellShares:
                print("bought1")

                spr = spr + ((max_bid - min_bid) * buy_list[0].bidShares)
                spread.save()
                buy = BuyTable.objects.get(pk=max_index)

                thisComp = Company.objects.get(name=buy.company)
                thisComp.sharePrice = buy.bidPrice
                thisComp.save()

                p1.cash = p1.cash - (int(buy.bidPrice) * int(buy.bidShares) * 1.05)
                p1.noShares = p1.noShares + buy_list[0].bidShares

                p2.cash = p2.cash + (int(buy.bidPrice) * int(buy.bidShares) * 0.95)
                p2.noShares = p2.noShares - buy_list[0].bidShares

                p1.save()
                p2.save()

                BuyTable.objects.get(pk=max_index).delete()
                SellTable.objects.get(pk=min_index).delete()

                u = UserTable.objects.filter(profile=p1)  # ,company=companyName)
                flagjoin = 0
                if u:
                    for i in u:
                        print(data_set["company"])
                        print(i.company)
                        if (i.company.name == buy.company.name):
                            u1 = UserTable.objects.get(profile=profile, company=i.company)
                            u1.noShares = u1.noShares + int(buy.bidShares)

                            u1.save()
                            flagjoin = 1
                            break

                    if (flagjoin == 0):
                        UserTable.objects.create(profile=profile,
                                                 company=Company.objects.get(name=buy.company),
                                                 noShares=buy.bidShares, pricesShare=buy.bidPrice)


                else:
                    UserTable.objects.create(profile=profile,
                                             company=Company.objects.get(name=buy.company),
                                             noShares=buy.bidShares, pricesShare=buy.bidPrice)


            elif buy_list[0].bidShares >= sell_list[0].sellShares:
                print("bought2")

                spr = spr + ((max_bid - min_bid) * sell_list[0].sellSharess)
                spread.save()
                buy = BuyTable.objects.get(pk=max_index)
                sell = SellTable.objects.get(pk=min_index)
                buy.bidShares = buy.bidShares - sell_list[0].sellShares
                buy.save()

                thisComp = Company.objects.get(name=buy.company)
                thisComp.sharePrice = buy.bidPrice
                thisComp.save()

                p1.cash = p1.cash - (int(buy.bidPrice) * int(sell.sellShares) * 1.05)
                p1.noShares = p1.noShares + sell_list[0].sellShares

                p2.cash = p2.cash + (int(buy.bidPrice) * int(sell.sellShares) * 0.95)
                p2.noShares = p2.noShares - sell_list[0].sellShares

                p1.save()
                p2.save()

                u = UserTable.objects.filter(profile=p1)  # ,company=companyName)
                flagjoin = 0
                if u:
                    for i in u:
                        print(data_set["company"])
                        print(i.company)
                        if (i.company.name == buy.company.name):
                            u1 = UserTable.objects.get(profile=profile, company=i.company)
                            u1.noShares = u1.noShares + int(buy.bidShares)

                            u1.save()
                            flagjoin = 1
                            break

                    if (flagjoin == 0):
                        UserTable.objects.create(profile=profile,
                                                 company=Company.objects.get(name=buy.company),
                                                 noShares=buy.bidShares, pricesShare=buy.bidPrice)


                else:
                    UserTable.objects.create(profile=profile,
                                             company=Company.objects.get(name=buy.company),
                                             noShares=buy.bidShares, pricesShare=buy.bidPrice)


                SellTable.objects.get(pk=min_index).delete()

            elif buy_list[0].bidShares <= sell_list[0].sellShares:
                print("bought3")

                spr = spr + ((max_bid - min_bid) * buy_list[0].bidShares)
                spread.save()
                s = SellTable.objects.get(pk=min_index)
                s.sellShares = s.sellShares - buy_list[0].bidShares
                s.save()
                buy = BuyTable.objects.get(pk=max_index)

                thisComp = Company.objects.get(name=buy.company)
                thisComp.sharePrice = buy.bidPrice
                thisComp.save()

                p1.cash = p1.cash - (int(buy.bidPrice) * int(buy.bidShares) * 1.05)
                p1.noShares = p1.noShares + buy_list[0].bidShares

                p2.cash = p2.cash + (int(buy.bidPrice) * int(buy.bidShares) * 0.95)
                p2.noShares = p2.noShares - buy_list[0].bidShares

                p1.save()
                p2.save()

                u = UserTable.objects.filter(profile=p1)  # ,company=companyName)
                flagjoin = 0
                if u:
                    for i in u:
                        print(data_set["company"])
                        print(i.company)
                        if (i.company.name == buy.company.name):
                            u1 = UserTable.objects.get(profile=profile, company=i.company)
                            u1.noShares = u1.noShares + int(buy.bidShares)

                            u1.save()
                            flagjoin = 1
                            break

                    if (flagjoin == 0):
                        UserTable.objects.create(profile=profile,
                                                 company=Company.objects.get(name=buy.company),
                                                 noShares=buy.bidShares, pricesShare=buy.bidPrice)


                else:
                    UserTable.objects.create(profile=profile,
                                             company=Company.objects.get(name=buy.company),
                                             noShares=buy.bidShares, pricesShare=buy.bidPrice)


                BuyTable.objects.get(pk=max_index).delete()


    UserHistory.objects.create(profile=profile,
                               company=Company.objects.get(name=data_set["company"]),
                               noShares=data_set["noShares"], pricesShare=data_set["Price"], buysell=0,
                               total=(int(data_set["Price"]) * int(data_set["noShares"]) * 0.95))
    context = {}
    z = dict(context, **returnDict(request))
    return render(request, "index.html", z)
