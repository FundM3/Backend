from rest_framework import serializers
from django.utils import timezone
from main.apps.profile.models import Profile
from main.apps.contribution.models import Contribution
from decimal import Decimal

TOKEN_SYMBOLS = {
    "0x249cE44C31090DE8946D343075F58EBD1799EF22": "USDC",
    "0x1345d63314bD37DB29dfBCe9e6e0c1489EAB4aC3": "USDC",
    "0xF42DD10Ea10dEb6dd9F79b26CFE7F408699B2224": "USDC",
    "0xDF2cd3C8888fFf246700BcC7C474c6C1A1C5A57A": "ETH",
    "0x7C183cf2Db16c999920a688409601E43D8b8fe73": "ETH",
    "0xf602da003C341Fe4afCa8922A168d96270f3F9bc": "ETH",
}

class RecordContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ['transaction_hash', 'token_address', 'sender_address', 'receiver_address', 'amount', 'origin_chain', 'destination_chain']

class ProfileSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Profile
        fields = ['name', 'profile_img', 'address']

class ContributionListSerializer(serializers.ModelSerializer):
    token_symbol =  serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    elapsed_time = serializers.SerializerMethodField()
    sender_profile = serializers.SerializerMethodField()

    class Meta:
        model = Contribution
        fields = ['transaction_hash', 'token_symbol', 'token_address', 'receiver_address', 'amount', 'origin_chain', 'destination_chain', 'sender_profile', 'elapsed_time']

    def get_amount(self, obj):
        amount_in_ether = Decimal(obj.amount) / Decimal('1e18')
        normalized_amount = amount_in_ether.quantize(Decimal('.00001')).normalize()
        return f"{normalized_amount:.5f}".rstrip('0').rstrip('.')

    def get_elapsed_time(self, obj):
        now = timezone.now()
        diff = now - obj.created_at
        if diff.days >= 365:
            return f"{diff.days // 365} years ago"
        elif diff.days >= 30:
            return f"{diff.days // 30} months ago"
        elif diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds >= 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "Just now"

    def get_sender_profile(self, obj):
        try:
            profile = Profile.objects.get(user__wallet_address=obj.sender_address)
            return ProfileSerializer(profile, context={'request': self.context.get('request')}).data
        except Profile.DoesNotExist:
            return {
                "name": "anonymous",
                "profile_img": "",
                "address": obj.sender_address
            }

    def get_token_symbol(self, obj):
        return TOKEN_SYMBOLS.get(obj.token_address, "Unknown")
