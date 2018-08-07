"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

Conner Swenberg, cls364 and Jay Chand, jpc342
12/8/17
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShipHeight(self):
        """
        Returns: ship's height in pixels
        """
        return self.height
    
    def getX(self):
        """
        Returns: x coordinate of ship's center
        """
        return self.x
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Creates a new ship using parent's init 
        """
        SHIP_X=GAME_WIDTH//2
        SHIP_Y=SHIP_BOTTOM+SHIP_HEIGHT//2
        GImage.__init__(self,x=SHIP_X, y=SHIP_Y, width=SHIP_WIDTH, height=SHIP_HEIGHT, source='ship.png')
        
    
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def moveship(self,inp):
        """
        A method to move the ship based on user input

        This method looks at user input, and moves the ship in the corresponding
        directions if the leftarrow or rightarrow keys are pressed.
        It also makes sure the ship will never go offscreen.

        Parameter inp: the user input
        Precondition: inp is an instance of GInput
        """
        if inp.is_key_down('left') and self.x>SHIP_WIDTH:
            self.x=self.x-SHIP_MOVEMENT
        if inp.is_key_down('right') and self.x<GAME_WIDTH-SHIP_WIDTH:
            self.x=self.x+SHIP_MOVEMENT
            
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired from alien and collides with ship
        
        Checks if any of the corners of the bolt are contained within the ship
        image to determine if there is a collision.
        
        Parameter bolt: a bolt object fired from an alien
        Precondition: bolt is a bolt object fired from an alien and on screen
        """
        velo=bolt.getBoltVelo()
        if velo<0:
            boltleft=bolt.getBoltX()-BOLT_WIDTH//2
            boltright=bolt.getBoltX()+BOLT_WIDTH//2
            bolttop=bolt.getBoltY()+BOLT_HEIGHT//2
            boltbottom=bolt.getBoltY()-BOLT_HEIGHT//2
            a=self.contains((boltleft,bolttop))
            b=self.contains((boltleft,boltbottom))
            c=self.contains((boltright,boltbottom))
            d=self.contains((boltright,bolttop))
            testlist=[a,b,c,d]
            if True in testlist:
                return True
        return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def powerupcollides(self,powerup):
        """
        Returns: True if powerup dropped by alien collides with ship
        
        Checks if any of the corners of the powerup are contained within the ship
        image to determine if there is a collision.
        
        Parameter powerup: a powerup object dropped by an alien
        Precondition: powerup is a powerup object dropped by an alien
        """
        powerupleft=powerup.getX()-POWERUP_WIDTH//2
        powerupright=powerup.getX()+POWERUP_WIDTH//2
        poweruptop=powerup.getY()+POWERUP_HEIGHT//2
        powerupbottom=powerup.getY()-POWERUP_HEIGHT//2
        a=self.contains((powerupleft,poweruptop))
        b=self.contains((powerupleft,powerupbottom))
        c=self.contains((powerupright,powerupbottom))
        d=self.contains((powerupright,poweruptop))
        testlist=[a,b,c,d]
        if True in testlist:
            return True
        return False

class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _width:     the width of the alien
    _height:    the height of the alien
    x:          x position of alien
    y:          y position of alien
    _source: source file for alien in Images folder
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    def setX(self,x):
        self.x=x
        
    def setY(self,y):
        self.y=y
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,n,col,row):
        """
        creates alien attributes to create alien
        Parameter n: indicates which alien source file to draw
        Precondition: n is an int between 0 and 2
        Parameter col: starting column of alien
        Precondition: col is an int >= 0
        Parameter row: starting row of alien
        Precondition: row is an int >= 0
        """
        assert isinstance(n,int) and len(ALIEN_IMAGES)>n>=0
        assert isinstance(col,int) and col>=0
        assert isinstance(row,int) and row>=0
        ALIEN_X=(ALIEN_WIDTH//2+ALIEN_H_SEP)+(ALIEN_WIDTH+ALIEN_H_SEP)*col
        ALIEN_Y=(GAME_HEIGHT-ALIEN_CEILING-ALIEN_HEIGHT//2-(ALIEN_HEIGHT+ALIEN_V_SEP)*
                 (ALIEN_ROWS-row-1))
        GImage.__init__(self, width=ALIEN_WIDTH, height=ALIEN_HEIGHT, x=ALIEN_X, y=ALIEN_Y, source=ALIEN_IMAGES[n])

        
    
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def boltcollides(self,bolt):
        """
        Returns: true if bolt was fired from player and collides with Alien
        
        Checks if any of the corners of the bolt are contained within the alien
        image to determine if there is a collision.
        
        Parameter bolt: a bolt object fired from a ship
        Precondition: bolt is a bolt object fired from a ship and on screen
        """
        velo=bolt.getBoltVelo()
        if velo>0:
            boltleft=bolt.getBoltX()-BOLT_WIDTH//2
            boltright=bolt.getBoltX()+BOLT_WIDTH//2
            bolttop=bolt.getBoltY()+BOLT_HEIGHT//2
            boltbottom=bolt.getBoltY()-BOLT_HEIGHT//2
            a=self.contains((boltleft,bolttop))
            b=self.contains((boltleft,boltbottom))
            c=self.contains((boltright,boltbottom))
            d=self.contains((boltright,bolttop))
            testlist=[a,b,c,d]
            if True in testlist:
                return True
        return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _objtype: determines if bolt belongs to alien or ship
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBoltX(self):
        return self.x
    
    def getBoltY(self):
        return self.y
    
    def getBoltVelo(self):
        return self._velocity
    
    def setBoltY(self,y):
        self.y=y
        
    
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,obj,xtrans=0):
        if isinstance(obj,Ship):
            BOLT_Y=obj.y+obj.height//2+BOLT_HEIGHT//2
            GRectangle.__init__(self,width=BOLT_WIDTH,height=BOLT_HEIGHT,x=obj.getX()+xtrans,y=BOLT_Y,fillcolor='red',linecolor='red')
            self._velocity=BOLT_SPEED
        if isinstance(obj,Alien):
            BOLT_Y=obj.y-obj.height//2-BOLT_HEIGHT//2
            GRectangle.__init__(self,width=BOLT_WIDTH,height=BOLT_HEIGHT,x=obj.getX(),y=BOLT_Y,fillcolor='red',linecolor='red')
            self._velocity=-BOLT_SPEED
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class Background(GImage):
    """
    A class to represent a background image.
    
    No new attributes besides those inherited from GImage.
    """
    def __init__(self, image):
        """
        Initializer for the class Background.
        
        Creates a GImage object that will serve as the game background.
        
        Parameter image: the image file to use as the background
        Precondition: image is a string representine a .png file
        """
        GImage.__init__(self, width=GAME_WIDTH, height=GAME_HEIGHT, x=GAME_WIDTH//2,
                        y=GAME_HEIGHT//2, source=image)

class Powerup(GImage):
    """
    A class to represent powerups dropped by aliens.
    
    ATTRIBUTES:
        _width:     the width of the powerup
        _height:    the height of the powerup
        x:          x position of powerup
        y:          y position of powerup
        source:    source file for powerup in Images folder
        _velocity:  velocity of powerup falling
        _type:      type of powers granted by powerup
    """
    # Getters and Setters:
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getVelo(self):
        return self._velocity
    
    def getType(self):
        return self._type
    
    def setY(self,y):
        self.y=y
    
    
    #Initializer:
    def __init__(self,alien,n):
        """
        Initializer for the Powerup class
        
        Parameter alien: alien that drops powerup once killed
        Precondition: alien is an alien object that drops the powerup upon
        collision with a ship bolt
        
        Parameter n: determines which image file to choose
        Precondition n: between 0 and len(POWERUP_IMAGE)
        """
        self._velocity=-POWERUP_SPEED
        if n==0:
            self._type='tribolt'
        if n==1:
            self._type='invincible'
        if n==2:
            self._type='extralife'
        GImage.__init__(self,width=POWERUP_WIDTH,height=POWERUP_HEIGHT,x=alien.getX(),y=alien.getY(),source=POWERUP_IMAGE[n])

    