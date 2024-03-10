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
                            
def execute_storyboard(story_context, current_snippet, get_input=get_user_input, send_output=print):
    current_record = create_context_record()
    while current_snippet is not None: 
        output, next_action, decision_function = current_snippet(story_context)
        current_record['snippets'] += [ current_snippet ]
        current_record['texts'] += [ output ]

        if next_action in ['input', 'end']:
            combined_texts = '\n'.join(current_record['texts'])
            send_output(combined_texts)
            story_context.append(current_record)

        if next_action == 'input':
            user_input = get_input(story_context)
            story_context[-1]['result'] = user_input
            current_record = create_context_record()
            current_snippet = decision_function(user_input)
        elif next_action == 'end':
            story_context[-1]['result'] = None
            return story_context
        else:
            current_snippet = next_action

