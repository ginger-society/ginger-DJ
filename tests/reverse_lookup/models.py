"""
Reverse lookups

This demonstrates the reverse lookup features of the database API.
"""

from gingerdj.db import models


class User(models.Model):
    name = models.CharField(max_length=200)


class Poll(models.Model):
    question = models.CharField(max_length=200)
    creator = models.ForeignKey(User, models.CASCADE)


class Choice(models.Model):
    name = models.CharField(max_length=100)
    poll = models.ForeignKey(Poll, models.CASCADE, related_name="poll_choice")
    related_poll = models.ForeignKey(
        Poll, models.CASCADE, related_name="related_choice"
    )
