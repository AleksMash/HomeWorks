from django.db import models
from datetime import datetime

director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
    (director, 'Директор'),
    (admin, 'Администратор'),
    (cook, 'Повар'),
    (cashier, 'Кассир'),
    (cleaner, 'Уборщик')
]

# CREATE TABLE PRODUCTS (
#     product_id INT AUTO_INCREMENT NOT NULL,
#     name CHAR(255) NOT NULL,
#     price FLOAT NOT NULL,
#
#     PRIMARY KEY (product_id)
# );

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)

# CREATE TABLE STAFF (
#     staff_id INT AUTO_INCREMENT NOT NULL,
#     full_name CHAR(255) NOT NULL,
#     position CHAR(255) NOT NULL,
#     labor_contract INT NOT NULL,
#
#     PRIMARY KEY (staff_id)
# );
class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            dif = self.time_out - self.time_in
        else:
            dif = datetime.now() - self.time_in
        return dif.total_seconds()//60

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount

# Create your models here.
