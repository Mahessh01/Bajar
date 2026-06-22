from django.db import models
from accounts.models import Account
from store.models import Product, Variation


# -------------------------
# PAYMENT MODEL
# -------------------------
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)

    # FIX: money should NOT be CharField
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payment_id)


# -------------------------
# ORDER MODEL
# -------------------------
class Order(models.Model):

    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    order_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=100, blank=True)
    order_note = models.CharField(max_length=200, blank=True)

    # FIX: float replaced with decimal
    tax = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # FIX: safe string (prevents crash if user is null)
        if self.user:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


# -------------------------
# ORDER PRODUCT MODEL
# -------------------------
class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # FIX: allow multiple variations (VERY IMPORTANT for your cart system)
    variations = models.ManyToManyField(Variation, blank=True)

    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)

    ordered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name