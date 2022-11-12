from direct.gui.DirectGui import *
from panda3d.core import *
from . import QuestPoster
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal

class QuestChoiceGui(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestChoiceGui')

    def __init__(self):
        DirectFrame.__init__(self, relief=None, parent=base.a2dLeftCenter, geom=DGG.getDefaultDialogGeom(), geom_color=Vec4(0.8, 0.6, 0.4, 1), geom_scale=(1.85, 1, 0.9), geom_hpr=(0, 0, -90), pos=(0.5, 0, 0))
        self.initialiseoptions(QuestChoiceGui)
        self.questChoicePosters = []
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.cancelButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.7, 1, 1), text=TTLocalizer.QuestChoiceGuiCancel, text_scale=0.06, text_pos=(0, -0.02), command=self.chooseQuest, extraArgs=[0])
        guiButton.removeNode()
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self)
        self.timer.setScale(0.3)
        #make a DirectScrolledList
        self.dScrollList = DirectScrolledList(
            parent = self,
            relief = None,
            pos = (0, 0, 0),
            incButton_pos=(.5, 0, .5), incButton_text="Inc",
            incButton_scale=0.3,
            decButton_pos=(-.5, 0, -.5), decButton_text="Dec",
            decButton_scale=0.3,
        )

        base.setCellsAvailable(base.leftCells, 0)
        base.setCellsAvailable([base.bottomCells[0], base.bottomCells[1]], 0)
        return

    def setQuests(self, quests, fromNpcId, timeout):
        for i in range(0, len(quests), 3):
            questId, rewardId, toNpcId = quests[i:i + 3]
            qp = QuestPoster.QuestPoster()
            qp.reparentTo(self)
            qp.showChoicePoster(questId, fromNpcId, toNpcId, rewardId, self.chooseQuest)
            self.questChoicePosters.append(qp)


        for qst in self.questChoicePosters:
            self.dScrollList.addItem(qst)

        self.timer.countdown(timeout, self.timeout)

    def chooseQuest(self, questId):
        if questId != 0:
            if config.GetBool('want-qa-regression', 0):
                self.notify.info('QA-REGRESSION: CREATEATASK: Create A Task.')
        base.setCellsAvailable(base.leftCells, 1)
        base.setCellsAvailable([base.bottomCells[0], base.bottomCells[1]], 1)
        self.timer.stop()
        messenger.send('chooseQuest', [questId])

    def timeout(self):
        messenger.send('chooseQuest', [0])
