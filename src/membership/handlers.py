from typing import Dict, Any, Optional

from .models import Membership
from user.models import User


def can_move_next_membership(
    user: User,
    achievement: Dict[str, Any],
    current_membership: Optional[Membership] = None,
    next_membership: Optional[Membership] = None,
):
    if 'total_completed_order' in achievement.keys():
        return handle_total_completed_order(
            user=user,
            total_completed_order=achievement['total_completed_order'],
            current_membership=current_membership, 
            next_membership=next_membership
        )


def handle_total_completed_order(
    user: User,
    total_completed_order: int,
    current_membership: Optional[Membership] = None,
    next_membership: Optional[Membership] = None,
):  
    if current_membership is None and next_membership is None:
        return False

    if current_membership:
        next_membership = current_membership.next_membership
    
    min_total_completed_order_rule = next_membership.rules.get('min_completed_order', None)
    if min_total_completed_order_rule is None:
        return False
    
    return total_completed_order >= min_total_completed_order_rule
    