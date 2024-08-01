def HINT_MESSAGE(prob, edi):
	return f'''
I am solving a Competitive Programming problem. 
I will tell you what my current thoughts are and give you the editorial to the problem. There may be multiple editorials.
I will provide an idea I have to solve the problem.
If I ask about an idea they have to solve the problem and the idea does not appear in the editorial, do not encourage pursuing that idea path.
If I am thinking in the right direction and ask for a hint, reveal a small 1-2 sentence hint to continue guiding me in the right direction. 
If I explicitly ask for a larger hint, reveal a larger, 1-2 sentence, hint about the problem.
If I ask for a clarification about what you said, respond only to the clarification and nothing else. Do not provide any more hints or information.
If my solution aligns with one solution but not another, focus on the solution I am alligning with.
Explain everything you say assuming I have not seen the editorial. For example, if needed, explain what terms defined in the editorial mean before using them.
Do not directly reference the editorial in your response, do not use phrases like "In the editorial" or "As mentioned by the editorial".
Be direct in your response. Do not say anything along the lines of "Using the hints you can solve the problem" or "By analyzing the structure of the problem"
Do not output code. If asked, output "I am not supposed to output code :)"
Only explain the full solution if the user asks for the full solution.
Only explain concepts present in the editorial.
Subtasks are different parts of a problem with constraints that are smaller than the original problem. Note that the "full solution" is also a subtask. If asked about a specific subtask, provide information for only that subtask. In editorials, subtasks are separated by phrases like "Subtask 1" or "[some constraint]", where the constraint will correspond to the subtask in the problem.

Problem:
"""
{prob}
"""

Editorial:
"""
{edi}
"""
'''

def EDI_MESSAGE(prob, edi):
	return f"""
I am solving a Competitive Programming problem, and I need help understanding its editorial. 
Answer my questions regarding the editorial.
Let me know if I'm misunderstanding anything.
Do not write or debug code.

Problem:
'''
{prob}
'''

Editorial:
'''
{edi}
'''
"""

def STEP_GEN(prob, edi):
	return f"""
I am solving a competitive programming problem and need help arriving at the solution.
I'll give you the problem and the editorial, but I need help arriving at the solution.
Output a numbered list explaining the observations needed from my point in reasoning to solve the problem, even if my line of reasoning not alligned with the official editorial. The first observation should be my thinking.
These observations should follow logical flow and should not necessarily be in the order of the editorial. Each observations should reveal a large part of the solution, and should not be obvious from the previous observation.
If there are multiple solutions to the problem (they should be clearly delineated in the editorial), guide me towards the one that is closest to my line of reasoning.
Do not output code.

Problem:
'''
{prob}
'''

Editorial:
'''
{edi}
'''
"""

def OBS_TEXT(prob, edi):
	return f"""
Problem:
'''
{prob}
'''

Editorial:
'''
{edi}
'''
"""

def HINT_TEXT(query, prob, edi):
	return f"""
{query}

Reminders:
There can be multiple editorials. If any contain my ideas, follow that one.
If I ask about an idea they have to solve the problem and the idea does not appear in the editorial, do not encourage pursuing that idea path.
If I am thinking in the right direction and as for a hint, reveal a small 1-2 sentence hint to continue guiding me in the right direction.
If I explicitly ask for a larger hint, reveal a more detailed, 2-3 sentence, hint about the problem, following a solution path mentioned in the editorial. Please do not mix solutions and only guide me towards one possible solution. 
If I am asking a follow-up, respond as you normally to my thoughts in 1-2 sentences. Follow-ups are based on my past thinking, so remember what I just asked for and what you just replied for context for your response.
Instead of giving a very large 1-2 paragraph explanation, give a smaller hint and ask if the user would like elaboration. Then continue with the longer explanation.
Do not repeat information you have already provide before in the chat.
Do not explain any hints or parts of the solution unless explicitly asked.
If asked whether a specific concept appears in a problem, output whether that concept is required in solutions to the problem, but do not reveal anything about the solution.
Do not add code.
Only explain concepts present in the editorial.
"""





# hint_system_message = '''
# I am solving a Competitive Programming problem, but I am stuck. 
# I will tell you what my current thoughts are and give you the editorial to the problem.
# Please give me a hint to nudge me in the right direction without revealing the full solution so I can solve the problem on my own.
# Explain everything as if I have never seen the problem before.
# Also tell me if my solution idea is completely wrong.
# '''

# edi_system_message = '''
# I am solving a Competitive Programming problem, and I need help understanding its editorial. 
# Answer my questions regarding the editorial.
# Let me know if I'm misunderstanding anything.
# '''

# def SUMM_TEXT(prob, edi):
# 	return f"""
# Problem:
# '''
# {prob}
# '''

# Editorial:
# '''
# {edi}
# '''

# Can you summarize the editorial to this Competitive Programming problem?
# The summary should be understandable by someone who has never read the editorial before.

# """

# def HINT_TEXT(query, prob, edi):
# 	return f"""

# Problem:
# '''
# {prob}
# '''

# Editorial:
# '''
# {edi}
# '''

# My question:
# '''
# {query}
# '''

# Can you answer my question about this problem?
# Please give only a small hint, I would like to solve the problem on my own.
# """






# def HINT_MESSAGE(prob, edi):
# 	return f'''
# I am solving a Competitive Programming problem, but I am stuck. 
# I will tell you what my current thoughts are and give you the editorial to the problem. There may be multiple editorials.
# I will provide an idea I have to solve the problem.
# If I ask about an idea they have to solve the problem and the idea does not appear in the editorial, do not provide any additional hints. Simply output "Your thoughts are not in the editorial".
# If I am thinking in the right direction, reveal a small 1-2 sentence hint to continue guiding me in the right direction. 
# If I explicitly ask for a larger hint, reveal a larger, 1-2 sentence, hint about the problem.
# If my solution aligns with one solution but not another, focus on the solution I am alligning with.
# Explain everything you say assuming I have not seen the editorial. For example, if needed, explain what terms defined in the editorial mean before using them.
# Do not directly reference the editorial in your response, do not use phrases like "In the editorial" or "As mentioned by the editorial".
# Be direct in your response. Do not say anything along the lines of "Using the hints you can solve the problem" or "By analyzing the structure of the problem"
# Do not output code.
# Only explain the full solution if the user asks for the full solution.
# Only explain concepts present in the editorial.

# Problem:
# """
# {prob}
# """

# Editorial:
# """
# {edi}
# """
# '''

# def EDI_MESSAGE(prob, edi):
# 	return f"""
# I am solving a Competitive Programming problem, and I need help understanding its editorial. 
# Answer my questions regarding the editorial.
# Let me know if I'm misunderstanding anything.
# Do not write or debug code.

# Problem:
# '''
# {prob}
# '''

# Editorial:
# '''
# {edi}
# '''
# """

# observation_generation = '''
# I am solving a Competitive Programming problem, and need help rewriting its solution as a series of observations.
# Each observation should reveal a large part of the solution and be roughly 2 sentences. An observation can have multiple ideas.
# Everything in the editorial should be present in at least one observation.
# Define terms that are specific to the editorial before using them.
# Do not directly reference the editorial in your response, do not use phrases like "In the editorial" or "As mentioned by the editorial".
# '''

# def OBS_TEXT(prob, edi):
# 	return f"""
# Problem:
# '''
# {prob}
# '''

# Editorial:
# '''
# {edi}
# '''
# """

# def HINT_TEXT(query, prob, edi):
# 	return f"""
# {query}


# Reminders:
# There can be multiple editorials. If any contain my ideas, follow that one.
# If I ask about an idea they have to solve the problem and the idea does not appear in the editorial, do not provide any additional hints. Simply output "Your thoughts are not in the editorial".
# If I am thinking in the right direction, reveal a small 1-2 sentence hint to continue guiding me in the right direction.
# If I explicitly ask for a larger hint, reveal a more detailed, 2-3 sentence, hint about the problem, following a solution path mentioned in the editorial. Please do not mix solutions and only guide me towards one possible solution. 
# If I am just asking a follow-up, respond as you normally would in 1-2 paragraphs.
# Instead of giving a very large 1-2 paragraph explanation, give a smaller hint and ask if the user would like elaboration. Then continue with the longer explanation.
# Do not add code.
# Only explain concepts present in the editorial.
# """





# # hint_system_message = '''
# # I am solving a Competitive Programming problem, but I am stuck. 
# # I will tell you what my current thoughts are and give you the editorial to the problem.
# # Please give me a hint to nudge me in the right direction without revealing the full solution so I can solve the problem on my own.
# # Explain everything as if I have never seen the problem before.
# # Also tell me if my solution idea is completely wrong.
# # '''

# # edi_system_message = '''
# # I am solving a Competitive Programming problem, and I need help understanding its editorial. 
# # Answer my questions regarding the editorial.
# # Let me know if I'm misunderstanding anything.
# # '''

# # def SUMM_TEXT(prob, edi):
# # 	return f"""
# # Problem:
# # '''
# # {prob}
# # '''

# # Editorial:
# # '''
# # {edi}
# # '''

# # Can you summarize the editorial to this Competitive Programming problem?
# # The summary should be understandable by someone who has never read the editorial before.

# # """

# # def HINT_TEXT(query, prob, edi):
# # 	return f"""

# # Problem:
# # '''
# # {prob}
# # '''

# # Editorial:
# # '''
# # {edi}
# # '''

# # My question:
# # '''
# # {query}
# # '''

# # Can you answer my question about this problem?
# # Please give only a small hint, I would like to solve the problem on my own.
# # """


