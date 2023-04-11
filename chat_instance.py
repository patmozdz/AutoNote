from notes import Note
import openai
from globals import GARBAGE_DIR


class ChatInstance:
    def __init__(self):
        self.chatgpt_info = None
        self.pre_prompt = "None"  # String so that it can be passed to ChatGPT without modification
        self.GPT_MODEL = "gpt-3.5-turbo"

        # TODO: Make it so that GPT can add subset notes with %%? Under 10 word summary?
        self.SYSTEM_MESSAGE = "You are tasked with creating notes based on text. Given an optional pre-prompt provided " \
                              "by the user, generate a concise list of notes summarizing the key points from the " \
                              "user-provided text. Use '%' instead of bullets for each note. Ensure you only include " \
                              "accurate information from the text, and do not add or make up any information. " \
                              "If it's appropriate to include outside information, precede it with " \
                              "'(generated information not in text):'."

        # Below makes it more readable because pre-prompt and user-provided text are on diff lines, but must remove whitespace
        self.QUERY_STRUCTURE = """
        Pre-prompt: {}
        User-provided text: {}""".strip()

        self.messages = []

    def make_initial_query(self, note: Note):
        # Change pre_prompt if the user wishes
        if input("Would you like to add any guidelines for this note? (Y/N) ") == "Y":
            self.pre_prompt = input("Enter the guidelines: ")

        formatted_query = self.QUERY_STRUCTURE.format(self.pre_prompt, note.og_text)

        assert len(self.messages) == 0

        self.messages.extend([
            {"role": "system", "content": self.SYSTEM_MESSAGE},
            {"role": "user", "content": formatted_query}
        ])

        self.chatgpt_info = openai.ChatCompletion.create(
            model=self.GPT_MODEL,
            messages=self.messages
        )

        # Remove the first % so that the bullet list is split properly
        response_text = self.chatgpt_info["choices"][0]["message"]["content"]

        self.messages.append({"role": "assistant", "content": response_text})

        if response_text.startswith("%"):
            response_text = response_text[1:]
        else:
            # TODO: Error because didn't start with % like it should?
            pass

        if response_text.endswith("%"):
            response_text = response_text[:-1]

        note.list_of_bulletpoints = [bullet.strip() for bullet in response_text.split("%")]

        print(f"Query: {formatted_query}\n\n"
              f"\t\t-----------------------------------------------------\n"
              f"\t\t{note.get_og_file_len()} second file turned into notes by ChatGPT:\n"
              f"\t\t-----------------------------------------------------")

        for bulletpoint in note.list_of_bulletpoints:
            print(f"-{bulletpoint}")

        print(f"\nNote creation: {note.get_datetime_stamp()}")

        note.move_og_file_to(GARBAGE_DIR)

    def follow_up_query(self):
        follow_up_text = input("Enter follow up text: ")

        self.messages.append({"role": "user", "content": follow_up_text})
        self.chatgpt_info = openai.ChatCompletion.create(  # TODO: Make it so that it saves each chat's info? chatgpt_info.append()?
            model=self.GPT_MODEL,
            messages=self.messages
        )
