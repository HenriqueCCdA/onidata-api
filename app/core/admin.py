from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Loan, Payment


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            None,
            {"fields": ("id",)},
        ),
        (
            _("User data"),
            {
                "fields": (
                    "user",
                    "register_ip",
                )
            },
        ),
        (
            _("Loan infos"),
            {
                "fields": (
                    "uuid",
                    "nominal_value",
                    "interest_rate",
                    "bank",
                )
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "created_at",
                    "modified_at",
                )
            },
        ),
    )

    list_display = (
        "id",
        "uuid",
        "user",
        "nominal_value",
        "interest_rate",
        "register_ip",
        "bank",
        "created_at",
        "modified_at",
    )

    readonly_fields = (
        "id",
        "uuid",
        "created_at",
        "modified_at",
    )

    list_display_links = (
        "id",
        "uuid",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            None,
            {"fields": ("id",)},
        ),
        (
            _("Payment infos"),
            {
                "fields": (
                    "uuid",
                    "loan",
                    "value",
                )
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "created_at",
                    "modified_at",
                )
            },
        ),
    )

    list_display = (
        "id",
        "uuid",
        "loan",
        "value",
        "created_at",
        "modified_at",
    )

    readonly_fields = (
        "id",
        "uuid",
        "created_at",
        "modified_at",
    )

    list_display_links = ("id", "uuid")
