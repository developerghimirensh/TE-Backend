from django.urls import path

from .views import TradeListCreateView, TradeDetailView


urlpatterns = [
    path(
        "",
        TradeListCreateView.as_view(),
        name="trade-list-create",
    ),

    path(
        "<int:pk>/",
        TradeDetailView.as_view(),
        name="trade-detail",
    ),
]