"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Conner Swenberg, cls364 ; Jay Chand, jpc342
12/8/17
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _moveright: determines if aliens should move right [True if yes, False if not]
        _firerate: random number between 1 and BOLT_RATE, changes after each new alien bolt created
        _stepcount: number of steps since last bolt fire from aliens [0.._firerate+1]
        _wavestate: state of wave, accessed by app.py
        _aliencounter: counts how many aliens we move, used to determine if no aliens left granting victory
        _score: a counter that keeps track of score, score is incremented when destroying aliens
        _newalienspeed: the new alien speed after increasing difficulty as user kills aliens
        _wavesleft: the number of waves remaining to beat the game [integer, 0<=wavesleft<=ALIEN_WAVES]
        _powerups: powerups currently on screen [list of Powerup, possibly empty]
        _poweruptime: determine at which amount of aliens left to drop powerup
        _tribolt: determine if powerup tribolt is engaged
        _invincible: determine if powerup invincible is engaged
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getState(self):
        """
        """
        return self._wavestate

    def setState(self,state):
        """
        """
        self._wavestate=state

    def getAliens(self):
        """
        """
        return self._aliencounter

    def getScore(self):
        """
        """
        return self._score

    def getLives(self):
        """
        """
        return self._lives

    def getPowerup(self):
        """
        """
        if self._triboltshots>0:
            return 'Tribolts left: '+str(self._triboltshots)
        if self._invincibletime>0:
            return 'Invincible: '+str(round(self._invincibletime,1))
        else:
            return '            '

    def getWavesleft(self):
        """
        Returns: the number of waves left to win the game
        """
        return self._wavesleft

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, lives=SHIP_LIVES, waves=ALIEN_WAVES, score=0):
        self._aliens=self.alienlist()
        self._ship=Ship()
        self._dline=GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],linewidth=1)#linecolor=)
        self._time=0
        self._moveright=True
        self._stepcount=0
        self._bolts=[]
        self._firerate=random.randint(1,BOLT_RATE)
        self._lives=lives
        self._wavestate=STATE_ACTIVE
        self._aliencounter=ALIEN_ROWS*ALIENS_IN_ROW
        self._score=score
        self._wavesleft = waves
        self._newalienspeed=ALIEN_SPEED
        self._newboltrate=BOLT_RATE
        self._powerups=[]
        self._poweruptime=random.randint(FIRST_POWERUP,ALIEN_ROWS*ALIENS_IN_ROW-1)
        self._triboltshots=0
        self._invincibletime=0


    def alienlist(self):
        """
        helper for __init__ to make 2D list of aliens
        Return: 2D list of alien objects
        """
        alienlist=[]
        n=0
        m=0
        for row in range(ALIEN_ROWS):
            rowlist=[]
            for col in range(ALIENS_IN_ROW):
                rowlist.append(Alien(m,col,row))
            alienlist.append(rowlist)
            n+=1
            m=n//(len(ALIEN_IMAGES)-1)
            if m>len(ALIEN_IMAGES)-1:
                n=0
                m=0
        return alienlist

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,view,state,inp,dt):
        if self._wavestate==STATE_ACTIVE:
            if self._ship!=None:
                self._ship.moveship(inp)
            self.makebolt(inp)
            if len(self._bolts)>0 and self._aliencounter>0:
                self.boltupdate()
            self.powerupupdate(dt)
            self._time=self._time+dt
            self.movealiens(self._newalienspeed - (WAVE_SPEED_INCREASE*(ALIEN_WAVES-self._wavesleft)))
            if self._aliencounter==0:
                self._wavestate=STATE_COMPLETE
            if self._lives<=0:
                self._wavestate=STATE_COMPLETE
                self._ship=None
        if state==STATE_CONTINUE:
            self._wavestate=STATE_ACTIVE
            self._ship=Ship()


    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    alien.draw(view)
        if self._ship!=None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            if self._aliencounter>0:
                bolt.draw(view)
        for powerup in self._powerups:
            powerup.draw(view)


    #HELPER METHODS FOR MOVING ALIENS
    def movealiens(self, speed):
        """
        Helper method that moves the alien array.

        This method uses helper methods (findrightedge and findleftedge) to find the rightmost and leftmost positions of the aliens every step, and it uses the helper movedirection to move all the aliens at once. The right and left edges help this method determine whether or not the aliens should keep moving in the direction they are, or move down and switch directions.

        Parameter speed: the speed at which the alien?s should be moving
        Precondition: speed is a float, 0<speed<=ALIEN_SPEED
        """
        rightedge=self.findrightedge()
        leftedge=self.findleftedge()
        if rightedge+ALIEN_H_SEP>GAME_WIDTH and self._moveright and self._time>=speed:
            self.movedirection('down')
            self.movedirection('left',ALIEN_H_SEP-(GAME_WIDTH-rightedge))
            self._moveright=False
        elif leftedge<ALIEN_H_SEP and not self._moveright and self._time>=speed:
            self.movedirection('down')
            self.movedirection('right',ALIEN_H_SEP-leftedge)
            self._moveright=True
        if self._moveright and self._time>=speed:
            self.movedirection('right')
        elif not self._moveright and self._time>=speed:
            self.movedirection('left')

    def findrightedge(self):
        """
        Returns: the rightmost edge of the alien wave

        Helper method that determines the rightmost edge of the alien list

        This function goes through every alien in the list,
        checks if it is not None, and assigns its x position plus half its width
        if its position is farthest to the right.
        """
        rightpos=0
        for col in range(ALIENS_IN_ROW):
            col=ALIENS_IN_ROW-1-col
            for row in self._aliens:
                if row[col]!=None:
                    rightpos=row[col].getX()+ALIEN_WIDTH//2
                    return rightpos
        return rightpos

    def findleftedge(self):
        """
        Returns: the leftmost edge of the alien wave

        Helper method for movealiens that determines the leftmost edge of the alien list

        This function goes through every alien in the list,
        checks if it is not None, and assigns its x position minus half its width
        if its position is farthest to the left.
        """
        leftpos=GAME_WIDTH
        for col in range(ALIENS_IN_ROW):
            for row in self._aliens:
                if row[col]!=None:
                    leftpos=row[col].getX()-ALIEN_WIDTH//2
                    return leftpos
        return leftpos

    def movedirection(self,direction,xchange=ALIEN_H_WALK,ychange=ALIEN_V_WALK):
        """
        A helper method that moves all living aliens in a single direction.

        This method uses for-loops to make every living alien move by changing its x or y positions. It also determines what happens when the aliens move down past the defense line (you lose the game). It also resets the hidden attribute self._time after every step, and increments self._stepcount.

        Parameter direction: the direction to move the aliens
        Precondition: direction is a string, either ?down?, ?right?, or ?left?

        Parameter xchange: the distance for the aliens to move in the x direction
        Precondition: xchange is an integer, 0<xchange<GAME_WIDTH

        Parameter ychange: the distance for the aliens to move in the y direction
        Precondition: ychange is an integer, 0<xchange<GAME_HEIGHT

        """
        self._aliencounter=0
        for row in self._aliens:
            for alien in row:
                if alien!=None:
                    alienx=alien.getX()
                    alieny=alien.getY()
                    if direction=='down':
                        alien.setY(alieny-ychange)
                        self._aliencounter=self._aliencounter+1
                        if alieny-ALIEN_HEIGHT//2<=DEFENSE_LINE:
                            self._wavestate=STATE_COMPLETE
                    if direction=='right':
                        alien.setX(alienx+xchange)
                        self._aliencounter=self._aliencounter+1
                    if direction=='left':
                        alien.setX(alienx-xchange)
                        self._aliencounter=self._aliencounter+1
        self._time=0
        self._stepcount+=1

    #HELPER METHODS FOR CREATING AND UPDATING BOLTS
    def chooseshooter(self):
        """
        Uses module random to generate a random int for the column of aliens to shoot from.

        From this column, a for-loop is used to pick the lowest alien. If there are no aliens in the column chosen, the method uses a recursive call to choose another column.

        To prevent infinite recursion, we only recursively call if aliens still exist on the screen.
        """
        col=random.randint(0,ALIENS_IN_ROW-1)
        for row in self._aliens:
            if row[col]!=None:
                shooter=row[col]
                return shooter
        if self._aliencounter!=0:
            return self.chooseshooter()
        return None

    def makebolt(self,inp):
        """
        Creates bolts from both the ship and the aliens.

        This function determines whether or not a ship bolt should be made by looking at user input, and whether or not alien bolts should be fired. The parameter inp represents user input, and it is provided as an argument when it is called by update (which takes inp as an argument when called by the update in app.py).

        Alien bolts depend on the bolt_rate, the number of steps the aliens have taken, and which alien should be firing. This method takes them all into account, and uses the helper method chooseshooter to determine which alien should be firing.

        Parameter inp: the user input
        Precondition: inp is an instance of GInput

        """
        shipcount=0
        for bolt in self._bolts:
            velo=bolt.getBoltVelo()
            if velo>0:
                shipcount+=1
        if shipcount<1 and inp.is_key_down('up') and self._ship!=None:
            self._bolts.append(Bolt(self._ship))
            if self._triboltshots>0:
                self._bolts.append(Bolt(self._ship,TRIBOLT_SEP))
                self._bolts.append(Bolt(self._ship,-TRIBOLT_SEP))
                self._triboltshots=self._triboltshots-1
            self.playSound('shipbolt')
        if self._stepcount>=self._firerate:
            shooter=self.chooseshooter()
            self._bolts.append(Bolt(shooter))
            self._stepcount=0
            self._firerate=random.randint(1,int(round(self._newboltrate)))
            self.playSound('alienbolt')

    def boltupdate(self):
        """
        Updates the positions of all the bolts in the lisrt of bolts on screen.

        Does this by looping through list of bolts and getting position and velocity
        to set a new y value.  Also calls checkcollision to check bolt collisions.
        """
        for bolt in self._bolts:
            bolty=bolt.getBoltY()
            if bolty>GAME_HEIGHT or bolty<0:
                del self._bolts[self._bolts.index(bolt)]
            bolty+=bolt.getBoltVelo()
            bolt.setBoltY(bolty)
        self.checkcollision()

    def checkcollision(self):
        """
        A method to check if any bolts fired from aliens collide with the ship

        This method simultaneously tracks collisions and which bolts are fired from the ship.  If a collision between an alien bolt and the ship is detected, The ship loses a life, the ship object is set to none,the bolt is removed from the list of bolts, Exploding sound made, the wave is paused, a penalty to score is applied.  Upon revival, the ship is granted a short period of invincibility time to recover.

        Also calls helper checkaliencollision to check if player bolts collide with aliens
        """
        shipbolts=[]
        for bolt in self._bolts:
            velo=bolt.getBoltVelo()
            if velo>0:
                shipbolts.append(bolt)
            check=False
            if self._ship!=None and velo<0:
                check=self._ship.collides(bolt)
            if check and self._invincibletime<=0:
                del self._bolts[self._bolts.index(bolt)]
                self._lives=self._lives-1
                self._wavestate=STATE_PAUSED
                self._ship=None
                self.playSound('shipexplode')
                self._invincibletime=RECOVERY_TIME
                self._score=self._score-SCORE_PENALTY
                self._triboltshots=0
        self.checkaliencollision(shipbolts)

    def checkaliencollision(self,shipbolts):
        """
        A method to check if any bolts fired from player collide with aliens.

        If a collision is detected between a player bolt and alien, the player?s score is increased
        (calls increase_score), a powerup is potentially dropped, the alien object is set to None,
        The bolt is removed from the list of bolts on screen, and a popping sound is made.

        Parameter shipbolts: the list of bolts fired from the ship
        Precondition: shipbolts is a list, each bolt has a velocity>0

        """
        for numrow in range(len(self._aliens)):
            for numalien in range(len(self._aliens[numrow])):
                check=False
                if len(shipbolts)>0 and self._aliens[numrow][numalien]!=None:
                    for bolt in shipbolts:
                        if self._aliens[numrow][numalien]!=None:
                            check=self._aliens[numrow][numalien].boltcollides(bolt)
                        if check and self._aliens[numrow][numalien]!=None:
                            self.increase_score(self._aliens[numrow][numalien])
                            self.increase_difficulty()
                            self.dropPowerup(self._aliens[numrow][numalien])
                            self._aliens[numrow][numalien]=None
                            del self._bolts[self._bolts.index(bolt)]
                            self.playSound('alienexplode')

    #HELPERS FOR ENHANCING GAMEPLAY
    def increase_score(self,alien):
        """
        Increases player?s score by a specified amount depending on which alien is blasted

        Parameter alien: alien that has just been blasted by player
        Precondition: alien has source file in ALIEN_IMAGE
        """
        if alien!=None:
            if alien.source=='alien1.png':
                self._score=self._score+10
            if alien.source=='alien2.png':
                self._score=self._score+20
            if alien.source=='alien3.png':
                self._score=self._score+40

    def increase_difficulty(self):
        """
        Makes aliens move faster by using a speed multiplier after each alien is blasted.
        Also increases the frequency of bolts shot by aliens.
        """
        if self._newalienspeed>ALIEN_MAX_SPEED:
            self._newalienspeed*=ALIEN_SPEED_INCREASE
        if self._newboltrate>BOLT_MAX_SPEED:
            self._newboltrate*=BOLT_SPEED_INCREASE

    def playSound(self,makesound):
        if makesound=='shipexplode':
            sound=Sound('blast1.wav')
        if makesound=='alienexplode':
            sound=Sound('pop1.wav')
        if makesound=='shipbolt':
            sound=Sound('pew2.wav')
        if makesound=='alienbolt':
            sound=Sound('pew1.wav')
        if makesound=='powerup':
            sound=Sound('pop2.wav')
        if makesound!=None:
            sound.play()

    def dropPowerup(self,alien):
        if self._aliencounter==self._poweruptime:
            n=random.randint(0,len(POWERUP_IMAGE)-1)
            if n!=2 and self._newalienspeed<ALIEN_MAX_SPEED:
                n=random.randint(0,len(POWERUP_IMAGE)-1)
            self._powerups.append(Powerup(alien,n))
            powertype=self._powerups[-1].getType()
            if self._aliencounter>1:
                self._poweruptime=random.randint(0,self._aliencounter//2)

    def powerupupdate(self,dt):
        if len(self._powerups)>0:
            for powerup in self._powerups:
                powerupy=powerup.getY()
                if powerupy<0:
                    del self._powerups[self._powerups.index(powerup)]
                powerupy+=powerup.getVelo()
                powerup.setY(powerupy)
                check=False
                if self._ship!=None:
                    check=self._ship.powerupcollides(powerup)
                if check:
                    powertype=powerup.getType()
                    if powertype=='tribolt':
                        self._triboltshots=TRIBOLT_SHOTS
                    if powertype=='extralife':
                        self._lives=self._lives+1
                    if powertype=='invincible':
                        self._invincibletime=INVINCIBLE_TIME
                    del self._powerups[self._powerups.index(powerup)]
                    self.playSound('powerup')
        if self._invincibletime>0:
            self._invincibletime=self._invincibletime-dt
