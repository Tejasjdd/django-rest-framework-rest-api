from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    TYPES=(
        ('HYDERABADI-BIRYANI','Hyderabadi-Biryani'),
        ('AMBUR-BIRYANI','Ambur-Biryani'),
        ('MEMONI-BIRYANI','Memoni-biryani'),
        ('THALASSERY-BIRYANI','Thalassery-biryani'),
        ('KASHMIRI-BIRYANI','Kashmiri-Biryani'),
        ('KOLKATA-BIRYANI','Kolkata-Biryani'),
    )
    SIZES=(
        ('HALF','half'),
        ('FULL','full'),
    )
    ORDER_STATUS=(
        ('PENDING','pending'),
        ('IN-TRANSIT','in-transit'),
        ('DELIVERED','delivered'),
    )

    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    types = models.CharField(max_length=20,choices=TYPES,default=SIZES[0])
    size = models.CharField(max_length=20,choices=SIZES,default=SIZES[0])
    order_status = models.CharField(max_length=20,choices=ORDER_STATUS,default='PENDING')
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Order {self.size} by {self.customer.id}"