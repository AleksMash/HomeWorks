from mc_donalds.models import *


cashier1 = Staff.objects.create(full_name = "Иванов Иван Иванович", position = cashier,
                                labor_contract = 1754)
cashier2 = Staff.objects.create(full_name = "Петров Петр Петрович",
                                position = cashier,
                                labor_contract = 4355)
direct = Staff.objects.create(full_name = "Максимов Максим Максимович",
                                position = director,
                                labor_contract = 1254)