from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import Event, Reservation
from events.serializers import EventSerializer, ReservationSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()

        status_param = self.request.query_params.get("status")
        venue_param = self.request.query_params.get("venue")

        if status_param:
            queryset = queryset.filter(status=status_param)

        if venue_param:
            queryset = queryset.filter(venue__icontains=venue_param)

        return queryset


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = Reservation.objects.all()

        event_id = self.request.query_params.get("event_id")

        if event_id:
            queryset = queryset.filter(event_id=event_id)

        return queryset

    @action(detail=True, methods=["POST"])
    def cancel(self, request, pk=None):
        reservation = self.get_object()

        if reservation.status == "cancelled":
            return Response(
                {"error": "Already cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation.event.available_seats += reservation.seats_reserved
        reservation.event.save()

        reservation.status = "cancelled"
        reservation.save()

        return Response(
            self.get_serializer(reservation).data,
            status=status.HTTP_200_OK,
        )
