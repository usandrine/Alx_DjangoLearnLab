# Update the follow method to create notification
@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
def follow(self, request, pk=None):
    user_to_follow = get_object_or_404(User, pk=pk)
    if request.user == user_to_follow:
        return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.follow(user_to_follow)
    
    # Create notification for followed user
    from notifications.models import Notification
    Notification.objects.create(
        recipient=user_to_follow,
        actor=request.user,
        verb='started following you'
    )
    
    return Response({'message': f'Now following {user_to_follow.username}'})