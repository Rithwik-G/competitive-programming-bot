from utils.scrapers import codeforces, usaco
from utils.chatbot import Chat
from utils.prompts import *
import os
import gradio as gr
import random
import time


dir_path = os.path.dirname(os.path.realpath(__file__))
CHAT_PATH = dir_path + '/saved_chats/'
used_ids = os.listdir(CHAT_PATH)

ind = 0
for i in used_ids:
	try:
		ind = max(ind, int(i.split('#')[1]))
	except:
		pass

chats = 500
last_update = time.time()

with gr.Blocks(title = "CP Helper Bot") as demo:
	ins = gr.Markdown("""
	# Usage Instructions
	First, paste a valid USACO (https://usaco.org) or codeforces (https://codeforces.com) problem link into the first text box input.
	Then, paste the link to an official editorial for the problem. Support for other platforms may (or may not) be coming soon.

	Choose between either 'hint' mode or 'editorial' mode


	## Hint Mode
	Chat with the bot about your ideas to solve the problem, and it will give you hints to guide your thinking.


	## Editorial Mode
	Chat with the bot about the editorial to the problem.

	# Feedback
	Please provide written feedback, maybe there was an issue with the bot or you really liked some response. You can give written feedback while chatting with the bot; it is recorded in real time with the chat history. Use the second text box for this.
	Please also provide feedback on the bot's helpfulness. Use the first dropdown (after you completed your chat) to rate how helpful the bot was. Consider how the bot's responses helped your understand faster and more effectively.
	
	Thanks for using this bot, and I hope you found it helpful!
				   
	This is an open source project maintained by [Rithwik Gupta](github.com/Rithwik-G) (beaboss on codeforces). If you would like to contribute (by adding scrapers for other OJs, adding features, adjusting prompts, making the feedback system better, etc.), you can make a pull request on HuggingFace community tab. If you want to collaborate, feel free to DM me on discord @Rithwik#1821 or at rithwikca2020@gmail.com.
	If you found this bot useful, please star the GitHub repo at.
	""")

	interface = gr.Chatbot(height='300px', placeholder="Provide a link for the problem you're solving.", 
		latex_delimiters = [{"left": "\\(", "right" : "\\)", 'display':False}, {"left": "$$$", "right" : "$$$", 'display':False}, {"left": "$", "right" : "$", 'display':False}])
	msg = gr.Textbox(label = "Chat with the bot")
	# clear = gr.ClearButton([msg, interface])
	state = gr.State()

	
	def cp_helper(message, history, state):
		global chats, last_update
		current_time = time.time()
		day = 24 * 60 * 60
		if (current_time - last_update >= day):
			last_update=current_time
			chats=1000

		if (chats <= 0):
			history.append((message, "Too many chats today, try again later."))
			return "", history, state

		chats-=1

		global ind
		if (state is None):

			# state = {'chatgpt': None,
			# 'problem_url': None,
			# 'edi_url' : None,
			# 'problem_text' : usaco.problem("https://usaco.org/index.php?page=viewproblem2&cpid=1421"),
			# 'edi_text' : usaco.editorial("", "https://usaco.org/current/data/sol_prob3_bronze_open24.html"),
			# 'first' : True,
			# 'style' : 'hint'}
			# state['chatgpt'] = Chat(HINT_MESSAGE(state['problem_text'], state['edi_text'])) # HINT_MESSAGE(state['problem_text'], state['edi_text'])
			# print('Edi', state['edi_text'])
			# assert(False)
			# state = {'chatgpt': None,
			# 'problem_url': None,
			# 'edi_url' : None,
			# 'problem_text' : codeforces.problem("https://codeforces.com/contest/1592/problem/E"),
			# 'edi_text' : codeforces.editorial("https://codeforces.com/contest/1592/problem/E", "https://codeforces.com/blog/entry/95583"),
			# 'first' : True,
			# 'style' : 'hint'}
			# state['chatgpt'] = Chat(HINT_MESSAGE(state['problem_text'], state['edi_text'])) # 
			# print(state['problem_text'], state['edi_text'])
			ind = random.randint(1, 100000)
			state = {'chatgpt': None,
			'problem_url': None,
			'edi_url' : None,
			'problem_text' : '',
			'edi_text' : '',
			'first' : True,
			'style' : None,
			'id': '#' + str(ind)}
			# state['chatgpt'] = Chat(HINT_MESSAGE(state['problem_text'], state['edi_text']))
			ind += 1
		bot = ""
		if (state['problem_text'] == ''):
			try:
				state['problem_url'] = message
				if ('usaco' in message.lower()):
					state['problem_text'] = usaco.problem(state['problem_url'])['statement']
				elif ('codeforces' in message.lower()):
					state['problem_text'] = codeforces.problem(state['problem_url'])['statement']
				else:
					assert(False)

				bot = "Thanks! Now could you provide a link to the editorial."
				print(state['problem_text'])
			except Exception as e:
				print(e)
				bot =  "There was something wrong with the link. Could you paste it again?"
		elif (state['edi_text'] == ''):
			try:
				state['edi_url'] = message
				if ('usaco' in message.lower()):
					# cbot = Chat(observation_generation)
					state['edi_text'] = usaco.editorial(state['problem_url'], state['edi_url'])
				elif ('codeforces' in message.lower()):
					# cbot = Chat(observation_generation)
					state['edi_text'] = codeforces.editorial(state['problem_url'], state['edi_url'])
				else:
					assert(False)

				assert(len(state['edi_text']))
				print('EDITORIAL\n', state['edi_text'])
				state['first']=True

				bot = "Would you like hints to help you solve the problem or an interactive explanation of the editorial (hint/editorial)? "
				
			except Exception as e:
				print(e)
				bot = "There was something wrong with the link. Could you paste it again?"

		elif (state['style'] == None):
			message = message.lower()
			if ('editorial' in message):
				state['style'] = 'editorial'
				state['chatgpt'] = Chat(EDI_MESSAGE(state['problem_text'], state['edi_text']))
				bot = state['edi_text'] + '\nLet me know if you have any questions.'
			elif ('hint' in message):
				state['style'] = 'hint'
				state['chatgpt'] = Chat(HINT_MESSAGE(state['problem_text'], state['edi_text']))
				bot += "What are you current thoughts on the problem? "
			else:
				bot += "Would you like hints to help you solve the problem or an interactive explanation of the editorial (hint/editorial)? "



		if (len(bot) == 0):
			if (state['style'] == 'hint'):
				if (state['first']):
					state['first']=False
					bot = state['chatgpt'].chat(HINT_TEXT(message, state['problem_text'], state['edi_text']))
				else:
					bot = state['chatgpt'].chat(HINT_TEXT(message, state['problem_text'], state['edi_text']))# + '\nExplain everything as if I have never seen the problem or editorial before in a maximum of 2 paragraphs.')
			else:
				state['first']=False
				bot = state['chatgpt'].chat(message + '\nExplain everything in a maximum of 2 paragraphs.')
					

		history.append((message, bot))

		chat_history = ''
		for i in history:
			chat_history += (f"USER: {i[0]}\n\nBOT: {i[1]}\n\n\n\n");
		
		with open(CHAT_PATH + state['id'], 'w') as f:
			f.write(chat_history)

		return "", history, state


	msg.submit(cp_helper, [msg, interface, state], [msg, interface, state])

	def sub_rating(state, option):
		if (state['id'] == None):
			return
		with open(CHAT_PATH + 'meta', 'a') as f:
			f.write(f"{state['id']}: {option}\n")

		return state, "Choose an Option"

	rating = gr.Dropdown([
		"Choose an Option",
		"1 - Very Unhelpful",
		"2 - Unhelpful",
		"3 - Neutral",
		"4 - Helpful",
		"5 - Very Helpful"
		], value = "Choose an Option", label='Rate the Conversation')

	gr.Interface(sub_rating, [state, rating], [state, rating], allow_flagging=False)

	def sub_feedback(state, message):
		if (state['id'] == None):
			return
		with open(CHAT_PATH + state['id'], 'a') as f:
			f.write(f"FEEDBACK: {message}\n\n\n\n")
		with open(CHAT_PATH + 'feedback', 'a') as f:
			f.write(f"FEEDBACK {state['id']}: {message}\n\n")

		return state, ""

	feedback = gr.Textbox(label = "Submit Feedback")
	feedback.submit(sub_feedback, [state, feedback], [state, feedback])

	


demo.launch()