# -*- coding=utf-8 -*-

import logging
from time import time

from django.http.response import Http404
from rest_framework import permissions
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from radarlivre_api.models import Airport, Flight, Observation, About, Notify, Collector, Airline, ADSBInfo
from radarlivre_api.models.serializers import AirportSerializer, FlightSerializer, ObservationSerializer,  \
    AboutSerializer, NotifySerializer, CollectorSerializer, \
    AirlineSerializer, ADSBInfoSerializer
from radarlivre_api.views.filters import ObservationPrecisionFilter, \
    ObservationFlightFilter, MapBoundsFilter, \
    ObservationLastTimestampFilter, MaxUpdateDelayFilter, AirportTypeZoomFilter


logger = logging.getLogger("radarlivre.log")


class CollectorList(ListCreateAPIView):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    filter_backends = (DjangoFilterBackend, MaxUpdateDelayFilter)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    

class CollectorDetail(APIView):
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    permission_classes = (permissions.DjangoModelPermissions,)
    
    def get_object(self, pk):
        try:
            return Collector.objects.get(pk=pk)
        except Collector.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        collector = self.get_object(pk)
        serializer = CollectorSerializer(collector, data=request.data)
        if serializer.is_valid():
            collector.timestamp = int(time() * 1000)
            collector.save()
        return Response(serializer.data)


class AirlineList(ListCreateAPIView):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    
class AirlineDetail(RetrieveUpdateDestroyAPIView):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = (permissions.IsAdminUser,)


class AirportList(ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = (DjangoFilterBackend, MapBoundsFilter, AirportTypeZoomFilter)
    filter_fields = ('prefix', 'name', 'country', 'state', 'city', 'latitude', 'longitude', 'type')
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    
class AirportDetail(RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (permissions.IsAdminUser,)


class FlightList(ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('airline', 'origin', 'destine')
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    
class FlightDetail(RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (permissions.IsAdminUser,)


class ADSBInfoList(APIView):
    queryset = ADSBInfo.objects.all()
    serializer_class = ADSBInfoSerializer
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,   
        ObservationPrecisionFilter,
        ObservationFlightFilter, 
        ObservationLastTimestampFilter
    )
    
    filter_fields = ('callsign')
    ordering_fields = '__all__'
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get(self, request, format=None):
        snippets = ADSBInfo.objects.all()
        serializer = ADSBInfoSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ADSBInfoSerializer(data=request.data)

        if serializer.is_valid():
            adsbInfo = serializer.save()

            # Generating a observation based in ADS-B info and updating collector
            # timestamp ...
            Observation.generateFromADSBInfo(adsbInfo)

        return Response(serializer.data)
    

class ObservationList(ListCreateAPIView):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        ObservationPrecisionFilter,
        ObservationFlightFilter,
        ObservationLastTimestampFilter
    )

    filter_fields = ('callsign')
    ordering_fields = '__all__'

class ObservationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    permission_classes = (permissions.IsAdminUser,)


class AboutList(ListCreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
    
class AboutDetail(RetrieveUpdateDestroyAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = (permissions.IsAdminUser,)

    
class NotifyList(ListCreateAPIView):
    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    
class NotifyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    permission_classes = (permissions.IsAdminUser,)
    