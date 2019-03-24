# Renju game with Artificial Intelligence

### Brief description
This project is an aggregate of Renju game engine and neural network, which knows how to play professionally. You can enjoy playing renju game via console interface and practice your skills.

### How to start
First of all, you should install this module. For example, use pip for this process.
After that you should **run sh-script renjuRL.sh**, which is located in the root directory (renjuRL_DK). Before running script check this script file has launch access rights.

After you are complete with launch, programm will run console interface environment and ask you to choose chip color.

Now you are ready to be introduced into interface commands.

### How to play
Your communications with game engine starts with game introducing message: <br/>
``` Your turn $: ``` <br/>
It is not allowed for you to give command without game invite.

There is a short list of valid commands:
* ```move x y``` <br/>
      x - horizontal coordinate (letter a - p, excluding i letter)<br/>
      y - vertical coordinate (digit 1 - 15)
      
      This command put chip into board cell with coordinates (x, y)
      
* ```show``` <br/>
      Unnecessary command, board updating is automatic

      This command update board drawing on the screen
      
* ```pass``` <br/>
      Add for expansion capability
      
      This command skip next move. Be carefull: two consecutive passes is a draw
      
* ```finish``` <br/>

      Thihs command finish current game
      
##### Remark
Dont worry about passing wrong command. Friendly user interface will give you a sign.
