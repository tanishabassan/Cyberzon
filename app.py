from flask import Flask, render_template, request, redirect, url_for
import openai

app = Flask(__name__)

counter = 1

def save_gpt4_response(gpt4_response):
    global counter
    file_name = f"responses/gpt4_response_{counter}.txt"
    with open(file_name, "w") as file:
        file.write(gpt4_response)
    counter += 1

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"].strip()

        messages = [
    {
        "role": "system",
        "content": f"Create a study plan for me to learn {topic}, structure 5 study session blocks that can be learned in 2 hours, in each study session include 3 things: topic of study session, outcome of study session and 3 links to resources to help study the topic, make sure the resources links are not dead links, try to make sure you find links that are not older than 2019, ensure these links are free and not something you have to pay for. Make sure your formatting is always consistent. In each study session, include the following format: \n\n'Study Session {{number}}:\nTopic: {{Topic Name}}\nOutcome: {{Outcome Description}}\n\nResources:\n1. {{Resource 1 Title}} ({{Resource 1 Year}}): {{Resource 1 URL}}\n2. {{Resource 2 Title}} ({{Resource 2 Year}}): {{Resource 2 URL}}\n3. {{Resource 3 Title}} ({{Resource 3 Year}}): {{Resource 3 URL}}'\n\n"
    },
    {
        "role": "system",
        "content": "You are an AI teacher, you always keep consistent formatting when providing the study session topics, outcomes and resources. You try to find the best resources that are not older than 2018 and are still active pages. You should always have 4 things in each study block, study session number, study session topic, study session outcome and study session resources. Your goal is to help the user learn any topic as easily as possible."
    }
]

        first = False
        while True:
            if first:
                question = input("> ")
                messages.append({"role": "user", "content": question})

            first = True

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages
            )

            content = response['choices'][0]['message']['content'].strip()

            print(f"{content}")
            messages.append({"role": "assistant", "content": content})
            save_gpt4_response(content)
            break

        return redirect(url_for("results"))

    return render_template("index.html")

@app.route("/results")
def results():
    global counter
    file_name = f"responses/gpt4_response_{counter - 1}.txt"
    with open(file_name, "r") as file:
        content = file.read()

    return render_template("results.html", content=content)

#if __name__ == "__main__":
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)
