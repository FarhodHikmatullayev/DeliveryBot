from datetime import datetime

from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name="Username")
    phone = models.CharField(max_length=13, null=True, blank=True, verbose_name="Telefon raqam")
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID", null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="F.I.Sh")
    location = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Manzil")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Foydalanuvchi qo'shilgan vaqt", null=True,
                                     blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Foydalanuvchi ma'lumotlari o'zgartirilgan vaqt",
                                      null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.full_name


class Order(models.Model):
    PAYMENT_METHODS = (
        ('naqt', "Naqt"),
        ('terminal', "Terminal"),
        ('click', "Click"),
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Buyurtmqa egasi", null=True, blank=True)
    products = models.TextField(null=True, blank=True, verbose_name="Mahsulotlar ro'yxati")
    created_at = models.DateTimeField(default=datetime.now(), verbose_name="Buyurtma berilgan vaqt", null=True,
                                      blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Buyurtma o'zgartirilgan vaqt", null=True, blank=True)
    payment = models.CharField(max_length=221, null=True, blank=True, choices=PAYMENT_METHODS,
                               verbose_name="To'lov shakli")

    class Meta:
        db_table = 'orders'
        verbose_name = "Order"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"{self.user} - {self.created_at}"


class Stock(models.Model):
    product_name = models.CharField(max_length=500, null=True, blank=True, verbose_name="Mahsulot nomi")
    products_url = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Aksiya linki")
    created_at = models.DateTimeField(verbose_name="Aktsiya yaratilgan vaqt", null=True,
                                      blank=True)

    class Meta:
        db_table = 'stock'
        verbose_name = "Stock"
        verbose_name_plural = "Aktsiyalar"

    def __str__(self):
        return f"{self.product_name}"
