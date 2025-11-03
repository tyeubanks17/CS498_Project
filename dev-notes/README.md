# To-do

## Individual Features
- Set editor - **Jacob**
- Study modes - 
- Set browser & filestructure - 
- Performance metrics & tracking - **Ty**

## Top Priorities - general
**DONE: Study set data structure**
- CSV, match Quizlet formatting
- Create Python class with file reader/writer method
- Find/create example study set(s)
- Must be able to handle special chars

**Priority #2: Look-and-feel conventions**
- Need consistent, documented look & feel
- Have collaborative meeting to establish look-and-feel
- Doesn’t need to be first priority – get functionality and basic layout down first
- Components: 
    - Button placement, size/shape
    - Tab ordering
    - General look-and-feel

## Task Notes
### Frontend/main menu
- Main menu screen for accessing all other screens/modes & browsing study sets
- Page for displaying study set, selecting a study mode

### Set editor
- Inserting/removing/reordering terms
- Tab navigation
- Inputting special chars
- Backend edit methods: insert/remove term, reorder term, edit term in-place
- Handling special chars: backend storage, frontend interface
  
### Study modes
- Handling user input (tab ordering, buttons, special chars)
- Designing modes/games
    - Allow studying term-first, definition-first, etc.
    - Handling ambiguity (some might have identical terms or definitions - should accept both)
### Set browser
- What does this look like? Organization options?
- Should entries be their own class?
- Set import/export: backend method + frontend interface
    - Allow pasting CSV text directly into GUI (along with file upload)
    - Allow importing from other file formats: .xlsx
### Performance metrics & tracking

## Other tasks
- Styling & graphic design

---

# SDLC Rules
The set of best practices to follow when contributing to the project. These are mostly just to keep people from stepping on each other's toes while developing.

1) Keep your work in your own branch.
Each feature should get its own branch

2) Each file should begin with a docstring
File docstrings should list: 
    1. the filename
    2. the purpose of the file
    3. the history of the file (creation date, revisions, etc.)

3) Each method should have a docstring
Method docstrings should list: 
    1. the purpose of the method
    2. the arguments of the method (including type and description)
    3. the return type/values of the method

## Naming conventions

https://peps.python.org/pep-0008/#prescriptive-naming-conventions

Just to keep these consistent.

- **Module file names**: short, lowercase, and all one word
- **Class names**: CapWords convention
- **Function & variable names**: lowercase, separated by underscores
- **Constants**: all uppercase, separated by underscores
