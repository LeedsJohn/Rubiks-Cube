Below is a brief overview of my CS-167 final project: John Cuber X-Treme.
The title is an inside joke that I have shared with my brother for several
years. I used to always tell him that I was going to make a Rubik's Cube
game and call it John Cuber X-Treme. After taking this computer science
class, I finally have the ability to bring my vision to life!

While I enjoy solving this Rubik's Cube, I believe it also serves as proof
that the Rubik's Cube can be made more accessible. When I was younger,
I found that it was incredibly difficult to learn how to solve the Rubik's
Cube. This is an interactive way to learn, and in addition, mistakes are
not an issue as you can easily reset. This can also serve as a replacement
to a physical Rubik's Cube if someone struggles to come by one for any
reason.

I would like to thank John Zelle for graphics.py and Professor
Janet Davis for inspiring my Button class and for her help and guidance
in this project and throughout the semester.

In addition, the background image I used throughout this project can be found
here:
wallpaperaccess.com/1280-x-720-cool

-------------------------------------------------------------------------------

POSSIBLE IMPROVEMENTS:
After looking at this project after another semester of computer science, 
there are a lot of changes I would make in the design of this project. If I
were to come back to this, some of the first changes I would make would be:
    1) Organizing the files
    2) Focusing more on object oriented programming
    3) Use a different GUI program than graphics.py
    4) Working to improve accessibility - I could add an "undo move" button
       and add color blind options, for example.
    5) Make it easier to rotate the Rubik's Cube

-------------------------------------------------------------------------------

INSTRUCTIONS TO RUN:
Run the main.py file. Click the buttons to select your game mode. The controls
for moving the cube are listed below.

-------------------------------------------------------------------------------
   
CONTROLS:
    The JKL keys apply the moves R, U, and F. The keys below JKL (M,.)
    apply a counterclockwise rotation (R', U', F')
    Similarly, the FDS keys apply the moves L, D, and B and VCX keys 
    apply a counterclockwise rotation (L', D', B')
    
    In order to rotate the cube, you use Y, H, and N to apply a z, y, and x
    rotation respectively. T, G, and B apply a counterclockwise rotation.
    
    Clockwise slice moves are handled with ;, A, and P (M, E, S).
    Counterclockwise slice moves are handled with /, Z, Q (M', E', S')
    
    While this might not be incredibly intuitive without experience with
    Rubik's Cubes, it is the standard.
    
    At any point, you can either click Give Up to see the cube solved
    or exit the program.
    
    To learn more about Rubik's Cube notation, please visit:
    https://jperm.net/3x3/moves

-------------------------------------------------------------------------------

GAMEMODES:
Solve: This gives you a scrambled Rubik's Cube. You win once it is solved.

Practice: This presents you with 8 options - options 1-7 allow you to practice
    the standard beginner steps to solve a Rubik's Cube. Free play gives you
    a solved Rubik's Cube to play with.
 
-------------------------------------------------------------------------------

BUGS:
After extensive testing, I have fixed every bug I could find. I do not know of
any existing bugs at the moment.

-------------------------------------------------------------------------------

FILE EXPLANATIONS:
    rubikscube.py:
        This is where I started - it contains a class representing a Rubik's
        Cube. It allows you to move the cube as well as check if several
        checkpoints along the solving process have been reached. Other notable
        functions can return the moves applied to the cube in a human readable
        format. It also can solve itself from cubesolver.
        
    rubikscubeUI.py:
        This holds most of the interface information. The Menu class assists
        in going through the menu sequence. The functions help draw the 
        Rubik's Cube and update it.
        
    cubesolver.py:
        This holds the class CubeSolver which can solve any Rubik's Cube. I
        have explained the algorithm I developed below.
        
    games.py:
        This file puts together many previous ones. The first class, CubeSetUp
        is used to put the cube in a state necessary for the different
        gamemodes. Then, the Play class presents the user with a cube
        to solve and waits for them to solve it (or exit).
    
    main.py:
        This file calls the menu sequence and play sequence to make the game
        playable.
        
    button.py:
        This file is very similar to the button.py written in class by
        Professor Janet Davis. However, it uses images to make buttons
        instead of rectangles. This gives them much more customizability.
        
    graphics.py:
        This file was provided in class and was written by John Zelle.
        It was used to create the GUI.
        
-------------------------------------------------------------------------------
 
SOLVING ALGORITHM:
    0. Rotate the cube until the yellow face is on top
        a) Perform z rotations 3 times - stop if yellow is on top at any point
        b) if that does not work, yellow must be on the B or F face so 
           x rotations until yellow is on top.
    
    1. Solve white edges
        a) Check if there are any white edges on the U face
            i) If there is one, check every U face / center combo until the UF
               sticker is white and the FU sticker matches the F sticker
               
        b) Check if there is a white edge in the center
            i) If there is one, rotate the cube until the white sticker is in
               the FR or FL position
               If it is the FR position:
                   R U R' to move to the top
               If it is in the FL position:
                   L' U' L to move to the top
            ii) As there is now a white edge on the U face (case 2a), return 
                to the the beginning of the step 2 algorithm.
                
        c) Check if there is a white edge on the U face but not the U sticker
            i) If there is one, rotate the cube until it's in the FU spot.
                R U' R' to move to the center
            ii) As there is now a white edge in the center position (case 2b),
                go back to the beginning of the step 2 algorithm
                
        d) Check if there is a white edge on the D face but not the D sticker
            i) If there is one, rotate the cube until the FD sticker is white
                F' to move it to the center
            ii) As there is now a white edge in the center position (case 2b),
                go back to the beginning of the step 2 algorithm
                
        e) Check if there is a misplaced white edge on the D face
            i) If there is, bring it to the top and go back to the beginning of
               the step 2 algorithm
        
        Repeat through these steps until the cross is solved
               
    2. Solve white corners
        a) Try to find a white corner on the U face
            i) Rotate the cube until it is over the correct spot
            ii) If the white sticker is in the FRU position: F' U' F
            iii) If the white sticker is in the RUF position: R U R'
            iv) If the white sticker is in the URF position: R2 U R2 U' R2
        
        b) Find misplaced corners in the D face
            i) Bring it to the top by inserting a yellow corner where it was
        
        Repeat through these steps until the white corners are solved
        
    3. Solve middle edges
        a) If there is an edge that only consists of combinations of
           green, orange, blue, and red on the U face:
           i) Rotate the cube until the FU sticker matches the F sticker
           ii) Insert it right or left depending on which center sticker
               matches the UF sticker
               
        b) If there is a misplaced edge in the E slice, insert a yellow edge
           where it is to bring it to the top
        
        Repeat these steps until the middle edges are solved
           
    4. Orient top edges (make the yellow cross)
        There are four cases 
            Already correct
            No edges facing up
            Line
            Adjacent edges
        
        Rotate the U face until one of these cases is found:
            Already correct: no moves necessary
            No edges facing up: F R U R' U' F' U2 F U R U' R' F'
            Line: F R U R' U' F'
            Adjacent edges: F U R U' R' F'
    
    5. Solve top edges (position them correctly)
        There are three cases
            Already correct
            Two edges correct relative to ecah other
            Z permutation
        
        Already correct: no moves necessary
        Two relatively correct: R U R' U R U2 R'
        Z permutation: M' U M2 U M2 U M' U2 M2
        
    6. Orient top corners (flip the yellow corners on top)
        For each corner, repeat R' D' R D until yellow is facing up
        
    7. Solve top corners
        There are four cases
            Already correct
            A permutation
            E permutation
            H permutation
        
        Already correct: do nothing
            A permutation
                Clockwise A: x L2 D2 L' U' L D2 L' U L'
                Counterclockwise A: x' L2 D2 L U L' D2 L U' L
            E permutation
                x' L' U L D' L' U' L D L' U' L D' L' U L D
            H permutation
                M2 U M2 U2 M2 U M2
        
        Perform U moves until the cube is solved
