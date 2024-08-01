import openai
from openai import OpenAI
import os
openai.api_key = os.environ['OPENAI_KEY']

class Chat:

	def __init__(self, system_message, lim=0.005):
		self.messages = [
			{"role": "system", "content" : system_message}
		]
		self.left = lim
		self.client = OpenAI(api_key=API_KEY)

	def chat(self, query):
		if (self.left <= 0):
			return "You have reached the chat limit."
		if (len(query) > 20000):
			return "Chat input is too long"

		self.messages.append({"role" : "user", "content" : query})
		
		# print(self.messages)

		response = self.client.chat.completions.create(
		  model="gpt-4o-mini",
		  messages=self.messages,
		  temperature=0.3
		)
		# del self.messages[-1]
		result = response.choices[0].message.content

		self.messages.append(response.choices[0].message)
		# print(response)
		# print([result])

		result = result.replace('\\(', '$')
		result = result.replace('\\)', '$')
		# print([result])

		self.left -= 0.6 * response.usage.completion_tokens / (10**6) + 0.15 * response.usage.prompt_tokens /(10**6)
		print(self.left)

		return (result)
