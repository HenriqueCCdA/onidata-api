from django.contrib import admin

from .models import Loan, Payment


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            "Primary key",
            {"fields": ("id",)},
        ),
        (
            "User data",
            {
                "fields": (
                    "user",
                    "register_ip",
                )
            },
        ),
        (
            "Loan infos",
            {"fields": ("uuid", "value", "rate", "contracted_period", "bank", "request_date")},
        ),
        (
            "Created and modified",
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
        "value",
        "rate",
        "contracted_period",
        "register_ip",
        "bank",
        "request_date",
        "created_at",
        "modified_at",
    )

    readonly_fields = (
        "id",
        "uuid",
        "request_date",
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
            "Primary key",
            {"fields": ("id",)},
        ),
        (
            "Payment infos",
            {
                "fields": (
                    "uuid",
                    "loan",
                    "value",
                    "payment_date",
                )
            },
        ),
        (
            "Created and modified",
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
        "payment_date",
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
