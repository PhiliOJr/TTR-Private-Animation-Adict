from .BattleBase import *
from .DistributedBattleAI import *
from toontown.toonbase.ToontownBattleGlobals import *
import random
from toontown.suit import DistributedSuitBaseAI
from . import SuitBattleGlobals, BattleExperienceAI
from toontown.toon import NPCToons
from toontown.pets import PetTricks, DistributedPetProxyAI
from direct.showbase.PythonUtil import lerp


class BattleGagTrackCalculator:

    def __init__(self, battleCalc, battle, gagTrack: int):
        self.battle = battle
        self.gagTrack = gagTrack
        self.battleCalc = battleCalc

    def damageCalc(self, toon, gagLvl: int):
        damage = getAvPropDamage(self.gagTrack, gagLvl, toon.experience.getExp(self.gagTrack), 0, 0, 0)
        damages = [0 for suit in self.battle.activeSuits]

        for i, suit in enumerate(self.battle.activeSuits):
            damages[i] = damage

            if self.gagTrack == LURE:
                self.calcLureEffect(suit, gagLvl, toon)

        return damages

    def calcLureEffect(self, target, atkLevel: int, toon):
        currLureId = -1
        rounds=5
        npcLurer=0
        toonId = toon.doId
        currLureId=self.battleCalc.addLuredSuitInfo(target.doId, -1, rounds, 0, toonId, atkLevel, lureId=currLureId, npc=npcLurer)
        targetLured=1
        self.battleCalc.successfulLures[target.doId]=[toonId, atkLevel, 100, -1]


