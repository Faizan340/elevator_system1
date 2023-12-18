from rest_framework import serializers
from elevator.models import ElevatorSystemModel, ElevatorModel, ElevatorRequestModel


class ElevatorSystemSerializer(serializers.ModelSerializer):
    """
    Serializer for ElevatorSystem
    """

    class Meta:
        model = ElevatorSystemModel
        fields = ['name', 'total_elevators', 'total_floors']

    def create(self, validated_data):
        """
        Overriding create method to create elevators for the elevator system.
        """
        elevator_system = ElevatorSystemModel.objects.create(**validated_data)
        total_elevators = validated_data.get('total_elevators')

        if total_elevators:
            for elevator_number in range(1, total_elevators + 1):
                ElevatorModel.objects.create(elevator_system=elevator_system, elevator_number=elevator_number)

        return elevator_system
    
    def validate_total_elevators(self, value):
        """
        Validating that the total number of elevators is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Total elevators must be a positive integer.")
        return value


class ElevatorSerializer(serializers.ModelSerializer):
    """
    Serializer for Elevator
    """

    class Meta:
        model = ElevatorModel
        fields = ['elevator_system', 'elevator_number', 'curr_floor', 'door_open', 'working', 'direction']


class ElevatorRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for ElevatorRequest
    """
    class Meta:
        model = ElevatorRequestModel
        fields = ['elevator', 'current_floor', 'destination_floor']
    
    def validate(self, data):
        """
        Validating the elevator's working status before creating a request.
        """
        elevator = data['elevator']

        if elevator.working == False:
            raise serializers.ValidationError("Elevator is not working. Request cannot be created.")

        return data
 
    def validate(self, data):
        """
        Validating the request data and update elevator status.
        """
        elevator = data['elevator']

        # Updating direction based on the destination floor
        if elevator.curr_floor < data['current_floor']:
            elevator.direction = 1  # Moving up
            elevator.door_open = False
        elif elevator.curr_floor > data['current_floor']:
            elevator.direction = -1  # Moving down
            elevator.door_open = False
        else:
            elevator.direction = 0  # No movement (elevator already on the requested floor)

        # Saving the changes to the elevator
        elevator.save()

        return data


    def validate_current_floor(self, value):
        """
        Validating that the current floor is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Current floor must be a positive integer.")
        return value

    def validate_destination_floor(self, value):
        """
        Validating that the destination floor is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Destination floor must be a positive integer.")
        return value


class ElevatorRequestWithElevatorSerializer(serializers.ModelSerializer):
    """
    Serializer for elevator request along with elevator's info.
    """
    elevator = ElevatorSerializer()

    class Meta:
        model = ElevatorRequestModel
        fields = ['elevator', 'current_floor', 'destination_floor']


class ElevatorWorkingSerializer(serializers.ModelSerializer):
    """
    Serializer for Elevator Working Status
    """
    class Meta:
        model = ElevatorModel
        fields = ['working']
        read_only_fields = ['elevator_system', 'elevator_number', 'curr_floor', 'door_open', 'direction']


class ElevatorDoorSerializer(serializers.ModelSerializer):
    """
    Serializer for Elevator Door
    """
    class Meta:
        model = ElevatorModel
        fields = ['door_open']
        read_only_fields = ['elevator_system', 'elevator_number', 'curr_floor', 'working', 'direction']
