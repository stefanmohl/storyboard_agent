def get_user_input():
    return input("Your choice: ")

def execute_storyboard(story_context, current_snippet, get_input=get_user_input, send_output=print):
    def create_context_record():
        return  {
                    'functions': [],
                    'texts': [],
                    'result': ""
                }
                            
    current_record = create_context_record()
    while current_snippet is not None: 
        output, next_action, decision_function = current_snippet(story_context)
        current_record['functions'] += [ current_snippet ]
        current_record['texts'] += [ output ]

        if next_action in ['input', 'end']:
            combined_texts = '\n'.join(current_record['texts'])
            send_output(combined_texts)

        if next_action == 'input':
            user_input = get_input()
            current_record['result'] = user_input
            story_context.append(current_record)
            current_record = create_context_record()
            current_snippet = decision_function(user_input)
        elif next_action == 'end':
            current_record['result'] = None
            story_context.append(current_record)
            return story_context
        else:
            current_snippet = next_action

