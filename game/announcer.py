from __future__ import unicode_literals
from enum import Enum

from direct.gui.OnscreenText import OnscreenText, Vec3, TextNode


class Color(tuple, Enum):
    Red = (1, 0.1, 0.1, 1)
    Blue = (0.15, 0.15, 1, 1)
    White = (1.0, 1.0, 1.0, 1.0)
    Orange = (1.0, 0.5, 0.0, 1.0)


def make_label(m, color):
    return OnscreenText(
        text=m, pos=Vec3(-1.2, .25, 0), scale=0.05,
        fg=color, align=TextNode.ALeft,
        # shadow=(0, 0, 0, 1),
    )


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
    _first_blood = False

    def __init__(self):
        self._messages = []

    def announce(self, message, color=Color.White, sfx=None):
        """Write the message to the screen and optionally play a sound effect.
        """
        # Add the label
        l = make_label(message, color)
        self._messages.append(l)

        # Layout the messages
        d = len(self._messages)
        for i, m in enumerate(self._messages):
            offset = max(5 - d, 0)
            # TODO: Animate these?
            m.setY((d - i + offset) / 15. + .5)

        if sfx:
            self._announcement = sfx

    def play_sound(self):
        # TODO: Use a priority system to play the most important sound
        if not self._announcement:
            return

        # The first sound is always "First Blood"
        if not self._first_blood:
            self._announcement = Announcement.FirstBlood
        self._first_blood = True

        # Load and play the sound
        sound = loader.loadSfx("sound/announcer/" + self._announcement)
        sound.play()

        # Reset the sound
        self._announcement = None

    def reset(self):
        for m in self._messages:
            m.removeNode()
        self._messages = []
        self._first_blood = False
