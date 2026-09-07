from django.urls import include, path


urlpatterns = [
    path(
        "api/accounts/",
        include("accounts.urls"),
    ),

    path(
        "api/trades/",
        include("trades.urls"),
    ),

    path(
        "api/analytics/",
        include("analytics.urls"),
    ),
]