from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ElevatorSystemViewSet, ElevatorViewSet, ElevatorRequestViewSet, ElevatorWorkingStatusView, ElevatorDoorStatusView

# app_name = "lift"

elevatorsystem_router = DefaultRouter()
elevatorsystem_router.register(r'elevatorsystems', ElevatorSystemViewSet)

elevator_router = DefaultRouter()
elevator_router.register(r'elevator', ElevatorViewSet)

elevatorrequest_router = DefaultRouter()
elevatorrequest_router.register(r'elevatorrequest', ElevatorRequestViewSet)


urlpatterns = [
    path('', include(elevatorsystem_router.urls)),
    path('', include(elevator_router.urls)),
    path('', include(elevatorrequest_router.urls)),
    path('elevators/<int:pk>/all_requests/', ElevatorViewSet.as_view({'get': 'all_requests'}), name='elevator-all-requests'),
    path('elevators/<int:pk>/calculate_next_destination/', ElevatorViewSet.as_view({'get': 'calculate_next_destination'}), name='elevator-calculate-next-destination'),
    path('elevators/<int:pk>/elevator_moving/', ElevatorViewSet.as_view({'get': 'elevator_moving'}), name='elevator-moving'),
    path('elevators/<int:pk>/elevator_working/', ElevatorWorkingStatusView.as_view(), name='elevator-working'),
    path('elevators/<int:pk>/elevator_door/', ElevatorDoorStatusView.as_view(), name='elevator-door'),
]
