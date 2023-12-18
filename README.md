PROJECT DESCRIPTION   :-  
The Elevator Management System is a web-based application designed to efficiently manage elevators in a building or complex. The system aims to streamline the elevator operations, provide real-time monitoring, and improve passenger experience while using the elevators.

ARCHITECTURE   :-
The project follows a Django architecture with the following components:

Elevator System Model: Represents the overall elevator system.
Elevator Model: Represents individual elevators with their status.
Elevator Request Model: Stores user requests for elevators.

ASSUMPTIONS   :-
The elevator system has one button per floor.
Immediate reflection of API calls to simulate real-time elevator movement.

TESTING   :-
Comprehensive unit tests have been written to ensure the functionality of each component. 

ELEVATOR SYSTEM INITIALIZATION   :-
The elevator system can be initialized by specifying the number of elevators, the total number of floors in the building, and other relevant details.

REQUEST QUEUE MANAGEMENT   :-
The system maintains a queue of elevator requests, ensuring fair distribution of elevator service among different floors.

NEXT DESTINATION PREDICTION   :-
The system predicts the next destination floor for each elevator based on its current floor, direction of travel.

ELEVATOR MAINTAINENCE AND STATUS UPDATES   :-
The system updates the status of each elevator based on its working condition.
Technologies used   :-  
Python, Django, Django Rest Framework, PostgreSQL.

API ENDPOINTS   :-

@ lift/elevator/

@ lift/elevatorsystems/

@ lift/elevatorrequest/

@ lift/elevators/pk/all_requests/   -   Fetching All requests for a given elevator.

@ lift/elevators/pk/calculate_next_destination/   -   Fetching next destination floor.

@ lift/elevators/pk/elevator_moving/   -   Fetching if the elevator is moving up or down.

@ lift/elevators/pk/elevator_working/   -   Marking a Elevator as working or not.

@ lift/elevators/pk/elevator_door/   -   Change the door status : open or close.
