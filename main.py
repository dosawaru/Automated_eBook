from openai import OpenAI
import json
from dotenv import load_dotenv

MAX_CHAPTERS = 10
MIN_CHAPTERS = 2

MAX_SUBHEADINGS = 4
MIN_SUBHEADINGS = 2
# Assuming you've set up the OpenAI API key as an environment variable.
load_dotenv()
client = OpenAI()

# Global flag to control whether to automatically proceed without user confirmation.
AUTO_PILOT = False

persona = "As an imaginative eBook writer, you excel at crafting engaging stories, building interesting plots, and developing relatable characters. Your writing style is characterized by creativity and a keen ability to connect with readers. Through your eBooks, you bring forth enjoyable and immersive experiences, making your narratives both entertaining and memorable. Your unique approach to storytelling sets you apart in the world of eBook creation, offering readers engaging content that resonates with a wide audience."

def create_chapters_for_title(title, num_chapters, num_subheadings):
    """
    Generate chapter names and subheadings for an eBook title.

    Parameters:
    - title (str): The title of the eBook.
    - num_chapters (int): The number of chapters to create.
    - num_subheadings (int): The number of subheadings for each chapter.
    """
    print(f"Creating chapters for the eBook titled '{title}'")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        max_tokens=3000,
        messages=[
            {"role": "system", "content": "Include 'json' to use 'response_format' of type 'json_object'..."},
            {"role": "user", "content": f"Write the chapters and subheadings for the ebook titled '{title}'. Make the chapter names as keys and the list of subheadings as values. Give at least {num_chapters} chapters and {num_subheadings} subheadings for each chapter."}
        ]
    )
    with open("chapters.json", "w") as chapters_file:
        print(response.choices[0].message.content)
        json.dump(json.loads(response.choices[0].message.content), chapters_file)


def create_chapter_content(title, chapter, subheading):
    """
    Generate content for a specific subheading under a chapter.

    Parameters:
    - title (str): The title of the eBook.
    - chapter (str): The name of the chapter.
    - subheading (str): The name of the subheading.

    Returns:
    - str: The generated content for the eBook.
    """

    print("-" * 50)
    print(f"Creating content for chapter '{chapter}' with subheading '{subheading}'")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        max_tokens=3000,
        messages=[
            {"role": "system", "content": f"" + persona + "The title of the eBook you are writing is '{title}'. Each chapter of the eBook has subheadings."},  # Omitted for brevity
            {"role": "user", "content": f"Write the text content for the subheading titled '{subheading}' under the chapter titled '{chapter}'. Be elaborate and clear. Include the chapter name and subheading in the response."}
        ]
    )
    print(f"Contents of the subheading: '{subheading}' under the chapter: '{chapter}' is \n")
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def main():
    title = input("Write the title of the eBook you'd like to generate: ")

    # Input validation for the number of chapters.
    while True:
        try:
            num_chapters = int(input(f"How many chapters would you like created? (Up to {MAX_CHAPTERS}): "))
            if MIN_CHAPTERS <= num_chapters <= MAX_CHAPTERS:
                break
            else:
                print(f"Please enter a number between {MIN_CHAPTERS} and {MAX_CHAPTERS}.")
        except ValueError:
            print("Please enter a valid number.")

    # Input validation for the number of subheadings.
    while True:
        try:
            num_subheadings = int(input(f"How many sub-heading chapters would you like created? (Up to {MAX_SUBHEADINGS}): "))
            if MIN_SUBHEADINGS <= num_subheadings <= MAX_SUBHEADINGS:
                break
            else:
                print(f"Please enter a number between  {MIN_SUBHEADINGS} and {MAX_SUBHEADINGS}.")
        except ValueError:
            print("Please enter a valid number.")

    satisfied = False
    while not satisfied:
        create_chapters_for_title(title, num_chapters, num_subheadings)
        satisfied = input("Are you satisfied with the created chapters? Press 'Y' for Yes or 'N' for No: ").lower() != 'n'

    chapters = None
    with open("chapters.json") as chapters_file:
        chapters = json.load(chapters_file)

    # Loop through chapters and subheadings to generate content.
    for chapter, subheadings in chapters.items():
        for subheading in subheadings:
            recreate = True
            while recreate:
                contents = create_chapter_content(title, chapter, subheading)
                recreate = not AUTO_PILOT and (input("Press 'N' to recreate the content if you are not satisfied. Press 'Y' to move on to the next subheading: ").lower() == 'n')
                if not recreate:
                    with open(f"{title}.txt", "a") as ebook_file:
                        ebook_file.write(contents + "\n\n")

    print("*" * 50)
    print(f"Completed generating the eBook '{title}'")

if __name__ == "__main__":
    main()
