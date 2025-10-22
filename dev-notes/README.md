# To-do

## Individual Features
- Set editor - **Jacob**
- Study modes - 
- Set browser & filestructure - 
- Performance metrics & tracking - **Ty**

## Top Priorities - general
**Priority #1: Study set data structure**
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
### Set editor
- Inserting/removing/reordering terms
- Tab navigation
- Inputting special chars
- Backend edit methods: insert/remove term, reorder term, edit term in-place
- Handling special chars: backend storage, frontend interface
- Highlight duplicate terms/definitions?
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

1) Never commit directly to master.
The `master` branch should always have a working version of our code on it. Integration should be taken care of in the `staging` branch. 
If you're not making code changes (e.g. just updating documentation), you can commit straight to `master`, but if it touches another person's work, be sure to get approval first. 
2) Keep your work in your own branch.
Each feature should get its own branch

## Naming conventions
https://peps.python.org/pep-0008/#prescriptive-naming-conventions
Just to keep these consistent.
**Module file names**: short, lowercase, and all one word
**Class names**: CapWords convention
**Function & variable names**: lowercase, separated by underscores
**Constants**: all uppercase, separated by underscores