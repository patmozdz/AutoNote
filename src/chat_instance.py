from notes import Note
import openai
from globals import GARBAGE_DIR


class ChatInstance:
    def __init__(self, parent_note: Note):
        self.parent_note = parent_note
        self.chatgpt_info = None
        self.pre_prompt = "None"  # String so that it can be passed to ChatGPT without modification
        self.GPT_MODEL = "gpt-4"

        # TODO: Make it so that GPT can add subset notes with %%? Under 10 word summary?
        with open("system message.txt") as txt_file:
            self.SYSTEM_MESSAGE = txt_file.read()

        # Below makes it more readable because pre-prompt and user-provided text are on diff lines, but must remove whitespace
        self.QUERY_STRUCTURE = """
        Pre-prompt: {}
        User-provided text: {}""".strip()

        self.messages = []

    def print_bullets(self):
        assert self.parent_note.list_of_bullets is not None

        print(f"Query: {self.messages[-2]['content']}\n\n"  # [-2] should be the last "role": "user" entry
              f"\t\t-----------------------------------------------------\n"
              f"\t\t{self.parent_note.get_og_file_len()} second file turned into notes by ChatGPT:\n"
              f"\t\t-----------------------------------------------------")

        for bulletpoint in self.parent_note.list_of_bullets:
            print(f"-{bulletpoint}")

        print(f"\nNote creation: {self.parent_note.get_datetime_stamp()}")

    def set_bullets_based_off_response(self, response_text):
        # Remove the first % so that split works properly
        if response_text.startswith("%"):
            response_text = response_text[1:]
        else:
            # TODO: Error because didn't start with % like it should?
            pass

        if response_text.endswith("%"):
            response_text = response_text[:-1]

        self.parent_note.list_of_bullets = [bullet.strip() for bullet in response_text.split("%")]

    def make_initial_query(self):
        # Change pre_prompt if the user wishes
        if input("Would you like to add any guidelines for this note? (Y/N) ") == "Y":
            self.pre_prompt = input("Enter the guidelines: ")

        formatted_query = self.QUERY_STRUCTURE.format(self.pre_prompt, self.parent_note.og_text)

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
        response_text = self.chatgpt_info["choices"][0]["message"]["content"]  # Can also be chatgpt_info.choices[0].message.content

        self.messages.append({"role": "assistant", "content": response_text})
        self.set_bullets_based_off_response(response_text)
        self.print_bullets()

        self.parent_note.move_og_file_to(GARBAGE_DIR)

        if input("Would you like to follow up? (Y/N)") == "Y":
            self.follow_up_query()

    def follow_up_query(self):
        follow_up_text = input("Enter follow up text: ")

        self.messages.append({"role": "user", "content": follow_up_text})
        self.chatgpt_info = openai.ChatCompletion.create(
            # TODO: Make it so that it saves each chat's info? chatgpt_info.append()?
            model=self.GPT_MODEL,
            messages=self.messages
        )

        response_text = self.chatgpt_info["choices"][0]["message"]["content"]
        self.set_bullets_based_off_response(response_text)
        self.print_bullets()

        if input("Would you like to follow up? (Y/N)") == "Y":
            self.follow_up_query()
