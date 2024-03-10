from engine import (execute_storyboard, find_snippet)
from ollama_connector import (storyboard2ollama, generate)
your_name = "" # Global variable for now, we should add this to event_sourcing

def snippet1(story_state):
    def decide_next(input):
        input = input.lower()
        if input == 'left': return snippet2
        if input == 'right': return snippet3
        return snippet4

    return ("You're at a crossroads. Go left or right?", 'input', decide_next)

def snippet2(story_state):
    return ("You find a treasure chest. You quickly open and loot it!", snippet3, None)

def snippet3(story_state):
    def choose(input):
        input = input.lower()
        if input == 'fight': return snippet5
        if input == 'flee': return snippet7
        return snippet6
    return ("You encounter a dragon. Fight or flee?", 'input', choose)

def snippet4(story_state):
    return ("You need to select one of the two: left or right.", snippet1, None)

def snippet5(story_state):
    return ("You are out of your mind! You try to fight the dragon. You died.", 'end', None)

def snippet6(story_state):
    return ("You are confused and stumble away from there.", snippet1, None)

def snippet7(story_state):
    treasure = ("\n...also, you are rich! How did that happen?"
                if find_snippet(snippet2, story_state) else "")
    return (f"You bravely run away. Congratulations{your_name}, you survived!{treasure}", 'end', None)

def snippet0(story_state):
    def record_name(input):
        if len(input.split()) > 2:
            return snippet_bad_name
        global your_name
        your_name = " " + input
        return snippet1
    return ("Please enter your name.", 'input', record_name)

def snippet_bad_name(story_state):
    return ("You need to say only your name, one or two words only. You can make up what you like.", snippet0, None)

def snippet8(story_state):
    def do_continue(input):
        input = input.lower() 
        if input == 'yes': return snippet1
        return snippetEnd
    return ("""A booming voice sounds from above:
HOW UNFORTUNATE, YOU ENDED UP WITHOUT TREASURE!
DO YOU WANT TO HAVE A BIT OF HISTORY UNDONE?""", 'input', do_continue)

def snippetEnd(story_state):
    return ("", 'end', None)

# =========================== OK, here we run the graph =======================

def main():
    initial_state = []
    initial_snippet = snippet0

    final_state = execute_storyboard(initial_state, initial_snippet, generate)

    if find_snippet(snippet5, final_state) or not find_snippet(snippet2, final_state):
        if find_snippet(snippet5, final_state):
            print(f"You died in stage {find_snippet(snippet5, final_state)}")
        if find_snippet(snippet2, final_state):
            print(f"You found treasure in stages {find_snippet(snippet2, final_state)}")
        final_state = final_state[:-1] # lets undo that undortunate end
        final_final_state = execute_storyboard(final_state, snippet8, generate)
    
    print(storyboard2ollama(final_state))
if __name__ == '__main__':
    main()
