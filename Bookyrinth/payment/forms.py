import re
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    city = forms.CharField()
    postal_code = forms.CharField()

    payment_method = forms.ChoiceField(
        choices=[
            ("card", "Credit / Debit Card"),
            ("paypal", "PayPal"),
            ("cod", "Cash on Delivery"),
        ],
        widget=forms.RadioSelect
    )

    # CARD FIELDS
    card_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "1234 5678 9012 3456",
            "maxlength": "16",
            "inputmode": "numeric"
        })
    )

    expiry = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "MM/YY",
            "maxlength": "5",
                "pattern": "(0[1-9]|1[0-2])\/[0-9]{2}",
        "title": "Enter expiry in MM/YY format"
    })
)

    cvv = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "123",
            "maxlength": "3",
            "inputmode": "numeric"
        })
    )

    # ---------------------------
    # VALIDATION LOGIC
    # ---------------------------

    def clean_card_number(self):
        number = self.cleaned_data.get("card_number")

        if number:
            if not number.isdigit():
                raise ValidationError("Card number must contain only digits.")
            if len(number) != 16:
                raise ValidationError("Card number must be exactly 16 digits.")

        return number

    def clean_cvv(self):
        cvv = self.cleaned_data.get("cvv")

        if cvv:
            if not cvv.isdigit():
                raise ValidationError("CVV must contain only digits.")
            if len(cvv) != 3:
                raise ValidationError("CVV must be exactly 3 digits.")

        return cvv

    def clean_expiry(self):
        expiry = self.cleaned_data.get("expiry")

        if expiry:
            # 1. Check format MM/YY
            if not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", expiry):
                raise ValidationError("Expiry must be in MM/YY format.")

            # 2. Extract month/year
            month, year = expiry.split("/")
            month = int(month)
            year = int(year)

            # Convert YY → YYYY (assume 2000–2099)
            current_year = datetime.now().year % 100
            current_month = datetime.now().month

            # 3. Expiry is in the past?
            if year < current_year:
                raise ValidationError("Card has expired.")

            if year == current_year and month < current_month:
                raise ValidationError("Card has expired.")

        return expiry

    def clean(self):
        cleaned_data = super().clean()

        payment_method = cleaned_data.get("payment_method")

        card_number = cleaned_data.get("card_number")
        expiry = cleaned_data.get("expiry")
        cvv = cleaned_data.get("cvv")

        # If card payment is selected, require all fields
        if payment_method == "card":
            if not card_number or not expiry or not cvv:
                raise ValidationError("All card details are required for card payment.")

        return cleaned_data