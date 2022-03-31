from celery import shared_task
from .models import Order
import datetime as dt

@shared_task
def complete_order(oid):
    order = Order.objects.get(pk = oid)
    order.complete = True
    order.save()



def clear_old():
    old_orders = Order.objects.all().exclude(time_in__gt=dt.datetime.now() - dt.timedelta(minutes = 5))
    old_orders.delete()

@shared_task
def say_hello():
    print('Hello my friend!')