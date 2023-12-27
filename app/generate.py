from .models import MCQ

def generator(file_path):
    question = None
    options = []
    answer = None
    

    with open(file_path, "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 5):
            data= lines[i:i+5]
            question = data[0].strip()
            for line in data:
                if line.startswith("Ans: "):
                    answer = line.replace('Ans: ', '').strip()
            options = [line.replace('Ans: ', '').strip() for line in data[1:] if line != ""]
            print(question)
            print(options)
            print(answer)
            mcq = MCQ(question=question, options=options, answer=answer, bangla=True)
            mcq.save()

            # Reset variables for the next question
            question = None
            answer = None
            options.clear()
            data.clear()