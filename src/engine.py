def get_user_input():
    return input("Your choice: ")

def execute_storyboard(story_context, current_snippet, get_input=get_user_input, send_output=print):
    output_accumulator = [] 
    while current_snippet is not None: 
        output, next_action, decision_function = current_snippet(story_context)
        output_accumulator += [(current_snippet, output)]

        if next_action in ['input', 'end']:
            combined_texts = '\n'.join([snip[1] for snip in output_accumulator])
            send_output(combined_texts)

        if next_action == 'input':
            user_input = get_input()
            story_context.append((output_accumulator, user_input))
            output_accumulator = []
            current_snippet = decision_function(user_input)
        elif next_action == 'end':
            story_context.append((output_accumulator, None))
            return story_context, None
        else:
            current_snippet = next_action

