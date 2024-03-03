import subprocess

# question = example "What is the weirdest..."
# type = one of the following ['Lessons learned from failures', 'Natural disaster experiences and aftermaths'...]
# adjective = one of the following [raunchy, scary, weird...]
# extra instuction is just if I wanted to add more sentences or not
def generateStory(question, type, adjective="", extraInstruction=""):
    prompt = f"""Create a {adjective} story that would be posted to reddit from a first person point of view. \
            The story must include {type}. The story has to answer the question: {question}. \
            Do not include a title. Do not talk to the auidence. There can be no fantsay. \
            Make the person telling the story tell very specific details.\
            Sometimes change perspective or to switch perspectives and to ponder about what is going on in another person's life. \
            Introduce the characters using the following exampled as a guide: "I, 27M", "Jeanne, 32F", and "John 16M". \
            Do not use the same names, same ages, or same genders, and use as many characters as you need. {extraInstruction}"""

    process = subprocess.Popen(['ollama', 'run', 'mistral'], 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True)

    # Send the prompt and assign the result
    answer = process.communicate(prompt + "\n")
    process.terminate()
    return answer[0]
    




