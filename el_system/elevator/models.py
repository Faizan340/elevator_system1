from django.db import models


class ElevatorSystemModel(models.Model):
    """
    Model for Elevator System
    """
    name = models.CharField(max_length=100)
    total_elevators = models.IntegerField(default=1)
    total_floors = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class ElevatorModel(models.Model):
    """
    Model for Elevator 
    """
    direction_choices = (
        (1, 'UP'),
        (-1, 'DOWN'),
        (0, 'STANDING STILL')
    )
    elevator_system = models.ForeignKey('ElevatorSystemModel', on_delete=models.CASCADE)
    elevator_number = models.IntegerField()
    curr_floor = models.IntegerField(default=1)
    door_open = models.BooleanField(default=True)
    working = models.BooleanField(default=True)
    direction = models.CharField(choices=direction_choices, default=0, max_length=100)

    def __str__(self):
        return str(self.elevator_number)


class ElevatorRequestModel(models.Model):
    """
    Model for Elevator Requests
    """
    elevator = models.ForeignKey('ElevatorModel', on_delete=models.CASCADE)
    current_floor = models.IntegerField()
    destination_floor = models.IntegerField()

    def __str__(self):
        return str(self.current_floor) +"to" + str(self.destination_floor)
