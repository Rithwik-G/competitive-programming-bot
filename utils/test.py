from chatbot import Chat 
from scrapers import usaco
from prompts import * 

prob = 'https://usaco.org/index.php?page=viewproblem2&cpid=1421'
edi = 'https://usaco.org/current/data/sol_prob3_bronze_open24.html'

prob_text = usaco.problem(prob)
edi_text = usaco.editorial(prob, edi)

chatbot = Chat(STEP_GEN(prob_text, edi_text))

# query = "I know the last element has to be a 1, because otherwise the minimum element won't be 1 which is impossible. I'm not sure how to proceed from here."
query = "I know that if I am given the first and last element of the original sequence, I can reconstruct it from the hint sequence. I'm not sure where to proceed from here."


query += '''
Only output a list explaining the observations needed from my point in reasoning, even if my line of reasoning not alligned with the official editorial.
The first observation should be my thinking, and then you should build the entire solution from there. Every subsequent observation should flow logically from my thinking.
'''
print(query)
print(chatbot.chat(query))