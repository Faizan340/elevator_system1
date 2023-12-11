from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from django.shortcuts import get_object_or_404

from .utils import get_elevator_object_or_404, success_response
from elevator.models import ElevatorSystemModel, ElevatorModel, ElevatorRequestModel
from elevator.serializers import (
    ElevatorSystemSerializer, ElevatorSerializer, ElevatorRequestSerializer,
    ElevatorRequestWithElevatorSerializer, ElevatorWorkingSerializer, ElevatorDoorSerializer
)


class ElevatorSystemViewSet(viewsets.ModelViewSet):
    """
    Model ViewSet for Elevator System
    """
    queryset = ElevatorSystemModel.objects.all()
    serializer_class = ElevatorSystemSerializer


class ElevatorViewSet(viewsets.ModelViewSet):
    """
    Model Viewset for Elevator.
    """
    queryset = ElevatorModel.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=True, methods=['GET'])
    def all_requests(self, request, pk=None):
        """
        Getting all elevator requests associated with the elevator.
        """
        elevator = get_elevator_object_or_404(pk, ElevatorModel)
        requests = ElevatorRequestModel.objects.filter(elevator=elevator)
        serializer = ElevatorRequestWithElevatorSerializer(requests, many=True)
        return Response(success_response(data=serializer.data))

    @action(detail=True, methods=['GET'])
    def calculate_next_destination(self, request, pk=None):
        """
        Calculating and returning the next destination floor for the elevator.
        """
        elevator = get_elevator_object_or_404(pk, ElevatorModel)
        elevator_system = elevator.elevator_system

        next_destination = (
            int(elevator.curr_floor) + 1
            if int(elevator.direction) == 1 and elevator.curr_floor < elevator_system.total_floors
            else int(elevator.curr_floor) - 1
            if int(elevator.direction) == -1 and elevator.curr_floor > 1
            else elevator.curr_floor
        )

        return Response(success_response(data={'next_destination_floor': next_destination}))

    @action(detail=True, methods=['GET'])
    def elevator_moving(self, request, pk=None):
        """
        Checking if the elevator is moving or not.
        """
        elevator = get_elevator_object_or_404(pk, ElevatorModel)
        moving_status = (
            'Elevator is moving up.'
            if int(elevator.direction) == 1
            else 'Elevator is moving down.'
            if int(elevator.direction) == -1
            else 'Elevator is not moving.'
        )
        return Response(success_response(message=moving_status))


class ElevatorBaseStatusView(generics.RetrieveUpdateAPIView):
    """
    Base APIView for Updating and Retrieving the Elevator Status.
    """
    queryset = ElevatorModel.objects.all()

    def get_object(self, pk):
        return get_elevator_object_or_404(pk, ElevatorModel)


class ElevatorWorkingStatusView(ElevatorBaseStatusView):
    """
    APIView for Updating and Retrieving the Elevator Working status.
    """
    serializer_class = ElevatorWorkingSerializer

    def get(self, request, pk, format=None):
        elevator = self.get_object(pk)
        serializer = ElevatorWorkingSerializer(elevator)
        return Response(success_response(data=serializer.data))

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                success_response(data=serializer.data, message="Elevator Working Status updated successfully"),
                status=status.HTTP_200_OK,
            )


class ElevatorDoorStatusView(ElevatorBaseStatusView):
    """
    APIView for Updating and Retrieving the Elevator Door status.
    """
    serializer_class = ElevatorDoorSerializer

    def get(self, request, pk, format=None):
        elevator = self.get_object(pk)
        serializer = ElevatorDoorSerializer(elevator)
        return Response(success_response(data=serializer.data))

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                success_response(data=serializer.data, message="Elevator Door Status updated successfully"),
                status=status.HTTP_200_OK,
            )


class ElevatorRequestViewSet(viewsets.ModelViewSet):
    """
    Model ViewSet for Elevator Requests.
    """
    queryset = ElevatorRequestModel.objects.all()
    serializer_class = ElevatorRequestSerializer
