from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='media/', blank=True, null=True) 

    def __str__(self):
        return self.name

class Option(models.Model):
    product = models.ForeignKey(Product, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    options = models.ManyToManyField(Option, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
class Cart(models.Model):
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def update_total(self):
        self.total_amount = sum(product.price for product in self.products.all())
        self.save()

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.TextField()
    mobile_number = models.CharField(max_length=15)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
