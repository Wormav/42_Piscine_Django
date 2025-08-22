#!/usr/bin/env python
"""
Test script for the reputation system
"""

import os

import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lpt_project.settings")
django.setup()

from lpt_app.models import CustomUser, Tip  # noqa: E402


def create_test_data():
    print("🚀 Creating test data for reputation system...")

    # Create test users
    users = []
    for i in range(1, 6):
        username = f"user{i}"
        if not CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.create_user(
                username=username, password="testpass123", email=f"user{i}@example.com"
            )
            users.append(user)
            print(f"✅ Created user: {username}")
        else:
            user = CustomUser.objects.get(username=username)
            users.append(user)
            print(f"👤 User already exists: {username}")

    # Create some tips
    tips_data = [
        "Always keep a backup of your important files",
        "Use keyboard shortcuts to save time",
        "Keep a water bottle at your desk to stay hydrated",
        "Take breaks every hour when working on a computer",
        "Use a standing desk to improve your posture",
    ]

    tips = []
    for i, content in enumerate(tips_data):
        if not Tip.objects.filter(content=content).exists():
            tip = Tip.objects.create(content=content, author=users[i])
            tips.append(tip)
            print(f"✅ Created tip by {users[i].username}: {content[:50]}...")
        else:
            tip = Tip.objects.get(content=content)
            tips.append(tip)
            print(f"📝 Tip already exists: {content[:50]}...")

    # Add some votes to create reputation
    print("\n🗳️ Adding votes to test reputation system...")

    # Give user1 lots of upvotes (should reach Elite level - 30+ points)
    for i in range(1, 5):  # users 2-5 upvote user1's tip
        if not tips[0].upvotes.filter(id=users[i].id).exists():
            tips[0].upvotes.add(users[i])
            print(f"👍 {users[i].username} upvoted {users[0].username}'s tip")

    # Give user2 moderate upvotes (should reach Moderator level - 15+ points)
    for i in [2, 3]:  # users 3-4 upvote user2's tip
        if not tips[1].upvotes.filter(id=users[i].id).exists():
            tips[1].upvotes.add(users[i])
            print(f"👍 {users[i].username} upvoted {users[1].username}'s tip")

    # Give user3 some downvotes (should have low/negative reputation)
    for i in [0, 1]:  # users 1-2 downvote user3's tip
        if not tips[2].downvotes.filter(id=users[i].id).exists():
            tips[2].downvotes.add(users[i])
            print(f"👎 {users[i].username} downvoted {users[2].username}'s tip")

    print("\n🔄 Updating permissions based on reputation...")

    # Update permissions for all users
    for user in users:
        old_reputation = user.reputation  # noqa: F841
        user.update_permissions()
        new_reputation = user.reputation

        print(f"🎯 {user.username}:")
        print(f"   Reputation: {new_reputation}")
        print(f"   Can downvote others: {user.can_downvote_others_tips()}")
        print(f"   Can delete tips: {user.can_delete_tips()}")
        print()


if __name__ == "__main__":
    create_test_data()
    print("✅ Test data creation completed!")
    print("\n📊 Current user standings:")
    for user in CustomUser.objects.all():
        rep = user.reputation
        if user.is_superuser:
            level = "👑 Admin"
        elif rep >= 30:
            level = "⭐ Elite"
        elif rep >= 15:
            level = "🔑 Moderator"
        else:
            level = "👤 User"

        print(f"{level} {user.username} - Reputation: {rep}")
