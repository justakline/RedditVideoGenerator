import subprocess


# type = one of the following [raunchy, scary, weird, suspenseful, painful, emotional, prideful, informative, tragic, bizarre, heartbreaking]
def generateStory(question, type):
    # with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        # Run the ollama command and redirect output to the temporary file
    # with open('ollama_output.txt', 'w+') as file:
    prompt = f"""Create a story that would be posted to reddit from a first person point of view. \
            The story must be {type}. The story has to answer the question: {question}. \
            Do not include a title. Do not talk to the auidence. There can be no fantsay. \
            Make the person telling the story tell very specific details.\
            Sometimes change perspective or to switch perspectives and to ponder about what is going on in another person's life. \
            Introduce the characters using the following exampled as a guide: "I, 27M", "Jeanne, 32F", and "John 16M". \
            Do not use the same names, same ages, or same genders, and use as many characters as you need. """

    process = subprocess.Popen(['ollama', 'run', 'mistral'], 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True)

    # Send the prompt and assign the result
    answer = process.communicate(prompt + "\n")
    process.terminate()
    return answer[0]
    



question = "What is the craziest thing that you have seen while driving in the middle of nowhere?"
print("\n\n" +question +"\n\nStory 1. Scary \n")
story = generateStory(question, "scary")
print (story)
# print(f"\n\n Story 2. Raunchy \n ")
# story = generateStory(question, "raunchy")
# print (story)