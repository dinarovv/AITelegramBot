admin_panel = '''\
<b>Admin panel</b> 
Enter key:
1. To switch model
2. To shutdown bot
q. To exit admin'''

def models_list(user):
    return f'''\
<b>Choose model</b>
Enter key:
1. gemma3:latest
2. deepseek-r1:1.5b
3. nomic-embed-text:latest
4. qwen2.5-coder:1.5b-base
5. llama3.1:8b
q. to stay on current model

<i>Current model: {user.model}</i>'''

hello_message = '''\
<b>Hello!</b> 
I am a telegram AI-assistant  with different language-models
My basic language-model is <b>gemma3</b>
Just send a message to start chatting with me!

<i>type '/help' if you need more info</i>'''

help_message = '''there is nothing now'''