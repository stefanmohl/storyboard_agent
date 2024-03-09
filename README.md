# storyboard_agent
An LLM agent system based on building storyboards programatically. A storyboard is a creative tool for authors and other creative writers (twinery.org is popular among authors of interactive fiction). You write snippets of text and link them together into sequences, using branches if you need them. This tool lets you build LLM agents by managing storyboards. You create minimal snippets that connect to each other, some that require input from the "user" (i.e. the LLM) to decide how the story progresses. A storyboard registers the context history. You can have multiple storyboards, corresponding to multiple agents, and you can manipulate the context history at will.

run `python src/snippets_treasure.py` to go on a bold adventure!
