from .models import reviewmodel

def RatingChartFeed(spot):
    review=reviewmodel.objects.filter(spot=spot)
    bel_avg=review.filter(rating='Below average').count()
    avg=review.filter(rating='Average').count()
    rec=review.filter(rating='Recomandable').count()
    goo=review.filter(rating='Good').count()
    fent=review.filter(rating='fentastic').count()
    lists=[bel_avg,avg,rec,goo,fent]
    total=sum(lists)
    perc=[]
    for i in lists:
        perc.append(int((i/total)*100))
    perc.append(total)
    return perc
   