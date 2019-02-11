# Renju game schedule

## Week 1:
        * Project game UI (graphical, console versions); choose instrument pack
        * Determine game state data format
        * Decompose software architecture
        * Create debug interface to communicate with a model
        (light console version, try to implement console game board displaying)

        * Create game engine
        * Prepare dummy architecture components
        (this way we will have working prototype of a model;
        constant prediction)

**TOTHINK:** Implement game engine in python (++); we are going to implement graphical UI in C# or similar lang.\
**Remark:** We should project painstakingly software architecture. There are a lot of scattered modules, we want to interact with them from other sources and from other modules in arch.\
**Remark:** Our model has to save its previous version (while training)

## Week 2:
        * Prepare dataset to train
        * Implement Policy network (and pretrain it)
        * Implement fast rollout policy (and pretrain it)
        * Implement value network (and pretrain it) 
        * Implement MCT mechanism
        * Implementing networks train and test interface;
        (project is quite big, we should create convinient interaction modules)

**Remark:** At this stage we don't need to have completely-trained model, our main goal is to have working prototype by this moment. Next stages we will improve networks incrementally

## Week 3:
        * Gather all modules in a complete system
        * Improve policy network (train on dataset)
        * Improve fast rollout policy
        * Improve value net
        * Improve policy network (let play with itself)

## Week 4:
        * Create graphical UI
        * Create console UI
        * Unite UI with game engine
        * Create bot (out model) request-engine; It has to communicate with game engine without our help ;)
**Reminder:** By the second week we have already had kind of console interface. 

## Week 5:
**Remark** This week allocated as a reserve time.
        
        * Produce UI crash-test
        * Test bot on a granny and a girlfriend
        * Have fun

**Remark:** It's important to win granny. If bot will do it, the tournament will be easy for it. ;)
        
