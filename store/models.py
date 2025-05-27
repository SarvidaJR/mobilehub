from django.db import models

# Create your models here.
class Phone(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='phones/')
    stock = models.PositiveIntegerField(default=0)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    PAYMENT_CHOICES = [
        ('full', 'Full Payment'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly (Every 3 Months)'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_bought = models.ForeignKey('Phone', on_delete=models.CASCADE)
    date_bought = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='full')

    def __str__(self):
        return f"{self.name} - {self.phone_bought.name}"

class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100, choices=[('on_the_spot', 'On the Spot'), ('loan', 'Loan')])
    status = models.CharField(max_length=100, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.phone.name} by {self.customer.name}"
    