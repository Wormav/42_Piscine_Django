#!/usr/bin/env python
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lpt_project.settings")
django.setup()

from lpt_app.models import CustomUser, Tip  # noqa: E402

# Add more votes to get someone to Elite level
user1 = CustomUser.objects.get(username="user1")
tip1 = Tip.objects.get(author=user1)

# Add more upvotes to reach 30+ reputation
users = CustomUser.objects.filter(username__in=["user4", "user5"])
for user in users:
    if not tip1.upvotes.filter(id=user.id).exists():  # type: ignore
        tip1.upvotes.add(user)
        print(f"👍 {user.username} upvoted {user1.username}'s tip")

# Create another tip for user1 and add votes to it
tip2 = Tip.objects.create(
    content="Always save your work frequently - Ctrl+S is your friend!", author=user1
)

# Add upvotes to this tip too
users_to_vote = CustomUser.objects.filter(username__in=["user2", "user3"])
for user in users_to_vote:
    tip2.upvotes.add(user)
    print(f"👍 {user.username} upvoted {user1.username}'s second tip")

user1.update_permissions()
print(f"\n🎯 {user1.username} final stats:")
print(f"   Reputation: {user1.reputation}")
print(f"   Can downvote others: {user1.can_downvote_others_tips()}")
print(f"   Can delete tips: {user1.can_delete_tips()}")

if user1.reputation >= 30:
    print("🎉 user1 has reached Elite level!")
else:
    print(f"📈 user1 needs {30 - user1.reputation} more points for Elite level")
