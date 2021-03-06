# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from protocol.api.serializers import ProtocolSerializer, AssignedProtocolSerializer
from protocol.models import Protocol, AssignedProtocol, ExecutedProtocol

from patients.models import Patient, CVPatient

from protocol_element.api.serializers import ProtocolElementSerializer, PEInquirySerializer
from protocol_element.models import ProtocolElement, PEInquiry

from accounts.models import Profile

from history.models import History

class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.all()
    serializer_class = ProtocolSerializer

    @list_route(methods=['post'])
    @transaction.atomic
    def createProtocol(self, request):
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        protocolElements = request.data.get('protocolElements', None)
        schedules = request.data.get('schedules', None)

        if (title == None or protocolElements == None or schedules == None or description == None):
            return Response({
                'error': "Invalid parameters"
            })

        protocol = Protocol.new(title=title, description=description, schedules=schedules)
        #Create elements
        for element in protocolElements:
            ProtocolElement.new(internalId=element["internalId"],
                                protocol=protocol,
                                type=element["type"],
                                elementData=element)
        #Create elements relations
        for element in protocolElements:
            if "nextElement" in element:
                if element["nextElement"] != '':
                    ProtocolElement.createConnectionsBetweenElements(internalId=element["internalId"],
                                                                     protocol=protocol,
                                                                     type=element["type"],
                                                                     elementData=element)
        return Response({"results": ProtocolSerializer(protocol).data})

    @list_route(methods=['post'])
    @transaction.atomic
    def editProtocol(self, request):
        protocolId = request.data.get('protocolID', None)
        title = request.data.get('title', None)
        description = request.data.get('description', None)
        protocolElements = request.data.get('protocolElements', None)
        schedules = request.data.get('schedules', None)

        if (protocolId == None or title == None or protocolElements == None or schedules == None or description == None):
            return Response({
                'error': "Invalid parameters"
            })

        protocol = Protocol.edit(id=protocolId, title=title, description=description, schedules=schedules)

        #My approach was, desativate all the elements and create news (this is not the best solution but the db space occupied is small)
        # Desativate all protocol elements
        allOldElements = ProtocolElement.all(protocol=protocol)
        for element in allOldElements:
            element.desativate()

        # Create elements
        for element in protocolElements:
            ProtocolElement.new(internalId=element["internalId"],
                                protocol=protocol,
                                type=element["type"],
                                elementData=element)
        # Create elements relations
        for element in protocolElements:
            if "nextElement" in element:
                if element["nextElement"] != '':
                    ProtocolElement.createConnectionsBetweenElements(internalId=element["internalId"],
                                                                     protocol=protocol,
                                                                     type=element["type"],
                                                                     elementData=element)
        return Response({"results": ProtocolSerializer(protocol).data})


    @list_route(methods=['post'])
    @transaction.atomic
    def run(self, request):
        patientId = request.data.get('patientID', None)
        protocolId = request.data.get('protocolID', None)
        inquiryData = request.data.get('inquiryData', None)

        if(patientId == None or protocolId == None or inquiryData == None):
            return Response({
                'error': "Invalid parameters"
            })

        physician = Profile.objects.get(user=request.user)
        patient = Patient.objects.get(id=patientId)
        CVPatient.addCVSet(inquiryData, patient)

        assignment = ExecutedProtocol.getNextExecution(patient)
        result = assignment.run(inquiryData=inquiryData, physician=physician)

        #Next assigment
        protocol = assignment.protocol
        last_execution = assignment.schedule_time
        ExecutedProtocol.new(protocol=protocol, patient=patient, physician=physician, last_execution=last_execution)

        return Response({"results": result})

    @list_route(methods=['post'])
    @transaction.atomic
    def runtest(self, request):
        protocolId = request.data.get('protocolID', None)
        inquiryData = request.data.get('inquiryData', None)

        if(protocolId == None or inquiryData == None):
            return Response({
                'error': "Invalid parameters"
            })

        protocol = Protocol.objects.get(id=protocolId)
        result, resultActions = protocol.run(inquiryData)

        return Response({"results": resultActions})

    @list_route(methods=['get'])
    def protocolInquiryComponents(self, request):
        patientid = self.request.query_params.get('patient', None)
        protocolid = self.request.query_params.get('protocol', None)

        if(patientid):
            patient = Patient.objects.get(id=patientid)
            assignment = ExecutedProtocol.getNextExecution(patient)
            protocol = assignment.protocol
        elif(protocolid):
            protocol = Protocol.objects.get(id=protocolid)
        else:
            return Response({
                'error': "Invalid parameters"
            })

        elements = ProtocolElement.all(protocol=protocol, type=ProtocolElement.INQUIRY)

        return Response({"results": {
                                "Protocol": ProtocolSerializer(protocol).data,
                                "Elements": PEInquirySerializer(elements, many=True).data}})

    @list_route(methods=['post'])
    @transaction.atomic
    def remove(self, request):
        protocolId = request.data.get('protocolID', None)

        if (protocolId):
            protocol = Protocol.objects.get(id=protocolId)
            protocol.remove()
        else:
            return Response({
                'error': "Invalid parameters"
            })

        return Response({"results": "success"})