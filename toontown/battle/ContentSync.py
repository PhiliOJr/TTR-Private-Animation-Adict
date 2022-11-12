from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import *
from toontown.toonbase import ToontownGlobals

class ContentSync:

    notify = directNotify.newCategory('ContentSync')

    def __init__(self, battle):
        self.battle = battle
        self.dmgCap = 0

    def sync(self, mxHP, dmgCap):
        for toon in self.battle.activeToons:
            rToon = self.battle.getToon(toon)
            if rToon:
                rToon.b_setMaxHp(mxHP)
                rToon.b_setHp(mxHP)

        self.dmgCap = dmgCap

        self.battle.setDmgCap(dmgCap)

