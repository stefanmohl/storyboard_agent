def find_snippet(test_snippet, story_context):
    locations = [i for i, snippet_list in enumerate(story_context)
                for snippet in snippet_list['snippets']
                if snippet == test_snippet ]
    return locations

def get_user_input(story_context):
    return input("Your choice: ")

def create_context_record():
    return  {
                'snippets': [],
                'texts': [],
                'result': ""
            }

def colour_printer(output):
    print(f"\n\u001b[31m{output}\u001b[0m")
                            
def run_storyboard(story_context, current_snippet, get_input=get_user_input, send_output=colour_printer):
    current_record = create_context_record()
    while current_snippet is not None: 
        output, action_type, next_action = current_snippet(story_context)
        current_record['snippets'] += [ current_snippet ]
        current_record['texts'] += [ output ]

        if action_type in ['input', 'end']:
            combined_texts = '\n'.join(current_record['texts'])
            send_output(combined_texts)
            story_context.append(current_record)

        if action_type == 'input':
            user_input = get_input(story_context)
            story_context[-1]['result'] = user_input
            current_record = create_context_record()
            current_snippet = next_action(user_input)
        elif action_type == 'end':
            story_context[-1]['result'] = None
            return story_context
        else:
            current_snippet = next_action

