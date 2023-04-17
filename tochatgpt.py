from globals import time_to_exit, to_chatgpt_q, GARBAGE_DIR, TO_PROCESS_DIR
import queue
from notes import Note
import threading
import openai  # To set API key, type in cmd/powershell: setx VARIABLE_NAME VARIABLE_VALUE /M

GPT_MODEL = "gpt-3.5-turbo"
# TODO: Make it so that GPT can add subset notes with %%? Under 10 word summary?
with file.open("system message.txt") as txt_file:
  SYSTEM_MESSAGE = txt_file.read()
                  
QUERY_STRUCTURE = """
Pre-prompt: {}
User-provided text: {}""".strip()


# Above makes it more readable because pre-prompt and user-provided text are on diff lines, but must remove whitespace


def generate_notes_query(pre_prompt, text):
    if pre_prompt is None:
        pre_prompt = "None"

    formatted_query = QUERY_STRUCTURE.format(pre_prompt, text)
    return formatted_query


def gpt_process_this(note: Note):  # TODO: Figure out how to continue messaging (do I have to store messages list myself?)
    query = generate_notes_query(note.pre_prompt, note.og_text)

    note.chatgpt_info = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": query}
        ]
    )

    # Remove the first % so that the bullet list is split properly
    response_text = note.chatgpt_info["choices"][0]["message"]["content"]
    if response_text.startswith("%"):
        response_text = response_text[1:]
    else:
        # Error because didn't start with % like it should?
        pass

    if response_text.endswith("%"):
        response_text = response_text[:-1]

    note.list_of_bulletpoints = [bullet.strip() for bullet in response_text.split("%")]

    print(f"Query: {query}\n\n"
          f"\t\t-----------------------------------------------------\n"
          f"\t\t{note.get_og_file_len()} second file turned into notes by ChatGPT:\n"
          f"\t\t-----------------------------------------------------")

    for bulletpoint in note.list_of_bulletpoints:
        print(f"-{bulletpoint}")

    print(f"\nNote creation: {note.get_datetime_stamp()}")

    note.move_og_file_to(GARBAGE_DIR)


def to_chatgpt_q_grabber():
    while not time_to_exit.is_set():
        try:
            # Default is block=True, but helps with clarity. Blocks for 1 second, then checks if time to exit before
            # continuing to try and get the front queue item (blocking for 1 second again)
            note = to_chatgpt_q.get(block=True, timeout=1)

            # New thread that's not daemon (so main waits for it to finish) that sets note object
            # self.gpt_notes attribute and self.topic attribute.
            gpt_processing_thread = threading.Thread(target=gpt_process_this,
                                                     daemon=False,
                                                     args=(note,),
                                                     name="gpt processing thread")
            gpt_processing_thread.start()

        except queue.Empty:  # Pass only if queue.Empty, ensures other exceptions are not caught
            pass


# Only run below if this is the main script running, mainly for testing.
if __name__ == "__main__":
    test_text = """The industrial revolution, which took place from the 18th to 19th centuries, was a period of 
significant technological and socioeconomic change. It marked the transition from agrarian, handicraft economies to 
those dominated by industry, machine manufacturing, and urbanization. The revolution began in Great Britain and 
eventually spread to the rest of the world, including the United States and Western Europe.
The introduction of steam power played a crucial role in the industrial revolution. Invented by Thomas Newcomen in 1712 
and later improved by James Watt, the steam engine became the driving force behind many new machines and innovations. 
Steam engines powered locomotives, steamships, and factory machinery, allowing for more efficient transportation and 
production methods. The development of the railway system connected cities and facilitated the movement of goods and 
people, leading to significant economic growth.
Another important development during the industrial revolution was the mechanization of textile production. The spinning 
jenny, invented by James Hargreaves in 1764, and the power loom, developed by Edmund Cartwright in 1784, revolutionized 
the textile industry. These innovations made it possible to mass-produce cloth at a faster pace and with less labor, 
resulting in lower costs and increased availability of textiles for the general population.
The industrial revolution also led to significant changes in the workforce. As factories were established and the demand 
for labor increased, many people moved from rural areas to cities to find work. This urbanization led to overcrowded 
living conditions, poor sanitation, and a variety of social issues. However, it also gave rise to the growth of the 
middle class, as more people found employment in skilled jobs and managerial positions. During this time, there was a 
focus on improving working conditions and labor rights. The Factory Acts, a series of laws passed in the United Kingdom, 
were designed to regulate the working hours and conditions for factory workers, particularly women and children. 
These laws aimed to improve the health and safety of workers and prevent the exploitation of child labor. In conclusion, 
the industrial revolution was a transformative period that brought about significant technological advancements and 
social changes. It led to the rise of industry, urbanization, and a shift in economic power, laying the groundwork for 
the modern world we live in today."""
    test_note = Note(test_text)
    gpt_process_this(test_note)

    while True:
        to_exec = input("Execute this code:")
        exec(to_exec)
