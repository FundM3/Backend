from django.db import models


class Contribution(models.Model):
    transaction_hash = models.CharField(max_length=70)
    token_address = models.CharField(max_length=42)
    sender_address = models.CharField(max_length=42)
    receiver_address = models.CharField(max_length=42)
    amount = models.DecimalField(max_digits=30, decimal_places=0, default=0)
    origin_chain = models.CharField(max_length=10)
    destination_chain = models.CharField(max_length= 10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_hash
