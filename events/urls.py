from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet, ReservationViewSet


router = DefaultRouter()

router.register("events", EventViewSet, basename="event")
router.register("reservations", ReservationViewSet, basename="reservation")


urlpatterns = [
    path("", include(router.urls)),
]
