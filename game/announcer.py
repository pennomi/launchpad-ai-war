from __future__ import unicode_literals
from enum import Enum


class Announcement(str, Enum):
    Carnage = "Carnage.wav"
    Dominating = "Dominating.wav"
    DoubleKill = "DoubleKill.wav"
    FirstBlood = "FirstBlood.wav"
    Godlike = "Godlike.wav"
    KillingSpree = "KillingSpree.wav"
    Massacre = "Massacre.wav"
    Mayhem = "Mayhem.wav"
    MegaKill = "MegaKill.wav"
    Ownage = "Ownage.wav"
    Rampage = "Rampage.wav"
    TripleKill = "TripleKill.wav"


class Announcer(object):
    _announcement = None

    def say(self, announcement):
        self._announcement = announcement

    def play_sound(self):
        if self._announcement:
            print(self._announcement)
            sound = loader.loadSfx("sound/announcer/" + self._announcement)
            sound.play()

    def reset(self):
        self._announcement = None
