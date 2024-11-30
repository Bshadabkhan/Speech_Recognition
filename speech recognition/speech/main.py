import openai
import os
import speech_recognition as sr
import pyttsx3
from agency_swarm import Agent
from agency_swarm.tools import CodeInterpreter, FileSearch
from agency_swarm.util.oai import set_openai_key

# Ensure OpenAI API key is set (using environment variable)
set_openai_key(os.getenv("Your Api key"))

# Create a Speech-to-Speech agent that uses Swarm AI
class SpeechToSpeechAgent(Agent):
    def __init__(self):
        super().__init__(
            name="SpeechToSpeechAgent",
            description="An AI assistant that listens to speech, queries OpenAI, and responds using speech.",
            tools=[CodeInterpreter, FileSearch],  # You can extend with more tools
            temperature=0.7,  # Set temperature for GPT response
            max_prompt_tokens=150,  # Control max tokens in response
        )
        self.recognizer = sr.Recognizer()  # Speech-to-text
        self.engine = pyttsx3.init()  # Text-to-speech engine
        self.engine.setProperty('rate', 150)  # Speech speed
        self.engine.setProperty('volume', 1)  # Speech volume

    def listen(self):
        """Listen to the user's speech and convert it to text."""
        with sr.Microphone() as source:
            print("Listening for speech...")
            # Adjust recognizer sensitivity to ambient noise levels
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)  # Convert speech to text
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand that. Could you repeat?")
                return None
            except sr.RequestError:
                self.speak("Sorry, I couldn't reach the speech service. Please try again later.")
                return None

    def speak(self, text):
        """Convert text to speech and speak it aloud."""
        print(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def query_openai(self, query):
        """Send a query to OpenAI GPT-4 and return the response."""
        try:
            response = openai.Completion.create(
                engine="gpt-4",  # GPT-4 model
                prompt=query,
                max_tokens=150,
                temperature=self.temperature,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Error interacting with OpenAI API: {str(e)}"

    def process_task(self, task):
        """Process a task using Swarm tools or interact with OpenAI."""
        if task == "analyze_data":
            # Example usage of CodeInterpreter tool
            return self.tools[0].run("Analyze this dataset: [1,2,3,4,5]")
        elif task == "search_files":
            # Example usage of FileSearch tool
            return self.tools[1].run("/path/to/files", "find report")
        else:
            # Default GPT query if no specific tool is required
            return self.query_openai(task)

    def run(self):
        """Main method for running the speech-to-speech agent."""
        while True:
            # Step 1: Listen to user speech
            user_input = self.listen()
            if user_input is None:
                continue  # Skip if no valid speech input

            # Step 2: Process task using Swarm AI or GPT-4
            gpt_response = self.process_task(user_input)

            # Step 3: Speak the response
            self.speak(gpt_response)

# Run the agent in a separate thread for better responsiveness
import threading

def run_agent():
    agent = SpeechToSpeechAgent()
    agent.run()

if __name__ == "__main__":
    agent_thread = threading.Thread(target=run_agent)
    agent_thread.start()
