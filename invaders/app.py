"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

Conner Swenberg, cls364 ; Jay Chand, jpc342
12/8/17
"""
import cornell
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _lastkeys:    the number key(s) pressed in the last frame [int>=0]
    _background:  the background image of the game [class: Background]
    _death:       used to express if the ship has run out of lives [bool]
    _newpara:     string used in STATE_INTRO to create visual and time spacing between writing lines [str]
    _intro:       the intro message to display on the screen when starting the game [str]
    _message:     message currently displayed on the screen starting as empty and finishing at _intro [str]
    _iwrite:      loop vairable in STATE_INTRO that increments each run through [0>=int>=WRITE_SPEED*len(self._message)]
    _jwrite:      loop variable in STATE_INTRO that increments every WRITE_SPEED run throughs [0>=int>=len(self._message)]
    """

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state=STATE_INACTIVE
        self._text=GLabel(text='Press s to play')
        self.GLabelstuff(self._text,60,'Arcade.ttf',GAME_WIDTH//2,GAME_HEIGHT//2,cornell.RGB(255, 255, 255))
        self._wave=None
        self._background = Background('space.png')
        self.draw()
        self._lastkeys=0
        self._pause='                                         '
        self._newpara='\n'+self._pause+'\n'
        self._intro=('<press spacebar to skip intro>'+self._newpara+'Hello starfighter..'+self._newpara+
                      'The American Galactic Force needs your help\n'+
                      'to defend our precious home from alien invaders..'+self._newpara+
                      'To engage with the enemy,\n use leftarrow and rightarrow keys to move\n'+
                      'and uparrow to fire laser bolts..'+self._newpara+
                      'Powerups will periodically drop from destroyed aliens..'+self._newpara+
                      'Good luck out there starfighter..'+self._pause)
        self._endmessage=''
        self._message=''
        self._iwrite=0
        self._jwrite=0
    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        STATE_INTRO: This state comes immediatly after starting up the game from STATE_INACTIVE.
        it displayes an introduction message to orient the player with the setting and also
        provides the game controls and that powerups are worth grabbing.  STATE_INTRO automatically
        enters STATE_ACTIVE after its message is complete, but can also be skipped by pressing
        spacebar.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        self._stateInfo()
        if self._state==STATE_INTRO:
            self._text=GLabel(text=self._message)
            self.GLabelstuff(self._text,30,'Arcade.ttf',GAME_WIDTH//2,GAME_HEIGHT//2,cornell.RGB(255, 255, 255))
            self.textwrite()
            if self._message==self._intro:
                self._state=STATE_NEWWAVE
        if self._state==STATE_NEWWAVE:
            self._wave=Wave()
            self._state=STATE_ACTIVE
        if self._state==STATE_ACTIVE:
            self.draw()
            self.view.clear()
            self._wave.update(self.view,self._state,self.input,dt)
        if self._state==STATE_PAUSED:
            self._text=GLabel(text='Press s to continue')
        if self._state==STATE_CONTINUE:
            self._wave.update(self.view,self._state,self.input,dt)
            self._state=STATE_ACTIVE
        if self._state==STATE_COMPLETE and self._wave.getLives()>0 and self._wave.getAliens()==0 and self._wave.getWavesleft()==0:
            self.view.clear()
            self._text=GLabel(text='You won!'+self._endmessage)
        if self._state==STATE_COMPLETE and self._wave.getLives()>0 and self._wave.getAliens()>0 and self._wave.getWavesleft()>=0:
            self.view.clear()
            self._text=GLabel(text='You lost :/'+self._endmessage)
        if self._state==STATE_COMPLETE and self._wave.getLives()==0:
            self.view.clear()
            self._text=GLabel(text='You lost :/'+self._endmessage)
        if self._state==STATE_COMPLETE and self._wave.getWavesleft()!=0:
            self.newwave()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        self._background.draw(self.view)
        if self._text!=None:
            self._text.draw(self.view)
        if self._state==STATE_NEWWAVE:
            self._wave.draw(self.view)
        if self._state==STATE_ACTIVE:
            self._text.text=('Lives: '+str(self._wave.getLives()) +
                             '   '+self._wave.getPowerup()+'   '+
                             'Score: '+str(self._wave.getScore()))
            self.GLabelstuff(self._text,40,'Arcade.ttf',GAME_WIDTH//2,GAME_HEIGHT-60,cornell.RGB(255,255,255))
            self._wave.draw(self.view)
        if self._state==STATE_PAUSED or self._state==STATE_COMPLETE:
            self._wave.draw(self.view)
            self.GLabelstuff(self._text,60,'Arcade.ttf',GAME_WIDTH//2,GAME_HEIGHT//2,cornell.RGB(255,255,255))


    # HELPER METHODS FOR THE STATES GO HERE

    def _stateInfo(self):
        """
        Called by update(), used to determine useful information depending on self._state.
        For STATE_INACTIVE, changes state from welcome screen to a new wave upon pressing 's'
        For STATE_PAUSED, changes state to STATE_CONTINUE upon pressing 's'
        For STATE_ACTIVE, gathers information on the current state of the wave and aliens left
        For STATE_INTRO, checks key presses to determine if the user wants to skip the intro
        For STATE_COMPLETE, creates the ending message to display and checks key presses
        to determine if user wishes to start over.
        """
        key_s=self.input.is_key_down('s')
        curr_keys=self.input.key_count
        change=key_s and curr_keys>0
        key_space=self.input.is_key_down('spacebar')
        change2=key_space and curr_keys>0
        if self._state==STATE_INACTIVE:
            self._text=GLabel(text='Press s to play')
            self.GLabelstuff(self._text,60,'Arcade.ttf',GAME_WIDTH//2,GAME_HEIGHT//2,cornell.RGB(255, 255, 255))
            if change:
                self._state=STATE_INTRO
            self._lastkeys= curr_keys
        if self._state==STATE_PAUSED:
            if change:
                self._state=STATE_CONTINUE
                self._wave.setState(self._state)
        if self._state==STATE_ACTIVE:
            self._state=self._wave.getState()
        if self._state==STATE_INTRO:
            if change2:
                self._state=STATE_NEWWAVE
        if self._state==STATE_COMPLETE:
            self._endmessage='\nScore: '+str(self._wave.getScore())+'\n<press spacebar>'
            if change2:
                self._state=STATE_INACTIVE


    def textwrite(self):
        """
        Helper method used to write the intro message in STATE_INTRO.
        Utilizes two loop variables to adjust the speed at which text is written.
        Adds to the message on screen by adding each character in the str self._intro
        and stops when the two messages are the same.
        """
        if self._jwrite<len(self._intro):
            if self._iwrite%WRITE_SPEED==0:
                self._message=self._message+self._intro[self._jwrite]
            self._iwrite+=1
            self._jwrite=self._iwrite//WRITE_SPEED

    def newwave(self):
        """
        A helper method that creates a new alien wave after completing the current wave.

        This method stores the user?s lives left and score before making a new wave
        (with a _wavesleft attribute that is one less than the previous wave,
        to make sure the next wave is harder than the first).
        It checks input (an attribute of the Invaders class) to see if the 's'
        key is pressed, and starts the new wave if it is.
        It is called by Invaders update.

        """
        self._text = GLabel(text='Wave Complete!\n Press s to continue')
        lives = self._wave.getLives()
        waves = self._wave.getWavesleft()
        score = self._wave.getScore()
        key_s=self.input.is_key_down('s')
        curr_keys=self.input.key_count
        change=key_s and curr_keys>0
        if change:
            self._wave = Wave(lives, waves-1, score)
            self._state = STATE_ACTIVE

    def GLabelstuff(self,obj,size,font,x,y,linecolor):
        """
        Helper function that changes the other attributes of a created GLabel

        Parameter obj: GLabel object to modify
        Precondition: obj is a valid GLabel with text already assigned to it

        Parameter size: size of text to set
        Precondition: size is an int>0

        Parameter font: choice of font to use for text
        Precondition: font is a valid font_name

        Parameter x: center x coordinate for GLabel text
        Precondition: x is an int, 0<x<GAME_WIDTH

        Parameter y: center y coordinate for GLabel text
        Precondition: y is an int, 0<y<GAME_HEIGHT

        Parameter color: color to set text to
        Precondition: color is a cornell.RGB or valid str in cornell module
        """
        obj.font_size=size
        obj.font_name=font
        obj.x=x
        obj.y=y
        obj.linecolor=linecolor
