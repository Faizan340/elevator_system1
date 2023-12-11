from django.test import TestCase
from rest_framework import serializers

from elevator.models import ElevatorSystemModel, ElevatorModel, ElevatorRequestModel
from elevator.serializers import (
    ElevatorSystemSerializer, ElevatorSerializer, ElevatorRequestSerializer,
    ElevatorRequestWithElevatorSerializer, ElevatorWorkingSerializer, ElevatorDoorSerializer
)


class ElevatorSystemSerializerTest(TestCase):
    def test_total_elevators_validation(self):
        serializer = ElevatorSystemSerializer(data={'total_elevators': -5})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Total elevators must be a positive integer.', serializer.errors['total_elevators'])

    def test_create_method(self):
        data = {'name': 'Test Elevator System', 'total_elevators': 3, 'total_floors': 5}
        serializer = ElevatorSystemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        elevator_system = serializer.save()

        self.assertEqual(ElevatorModel.objects.filter(elevator_system=elevator_system).count(), 3)


class ElevatorRequestSerializerTest(TestCase):
    def test_validate_current_floor(self):
        serializer = ElevatorRequestSerializer(data={'current_floor': -1, 'destination_floor': 3})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Current floor must be a positive integer.', serializer.errors['current_floor'])

    def test_validate_destination_floor(self):
        serializer = ElevatorRequestSerializer(data={'current_floor': 1, 'destination_floor': 0})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Destination floor must be a positive integer.', serializer.errors['destination_floor'])
