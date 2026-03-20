from django.shortcuts import render
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_view(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    chat_history = request.session["chat_history"]

    if request.method == "POST":
        user_input = request.POST.get("message")

        chat_history.append({"role": "user", "content": user_input})

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history
        )

        respuesta = res.choices[0].message.content

        chat_history.append({"role": "assistant", "content": respuesta})

        request.session["chat_history"] = chat_history

    return render(request, "chat/index.html", {"chat_history": chat_history})