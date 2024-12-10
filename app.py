import gradio as gr
from huggingface_hub import InferenceClient
from llama_cpp import Llama
from llama_cpp.llama_chat_format import MoondreamChatHandler

chat_handler = MoondreamChatHandler.from_pretrained(
    repo_id="vikhyatk/moondream2",
    filename="*mmproj*",
)

model_name = "volumetrader/model"

llm = Llama.from_pretrained(
    repo_id=model_name,
    filename="unsloth.Q4_K_M.gguf",
    chat_handler=chat_handler,
    n_ctx=2048,
)

"""
For more information on `huggingface_hub` Inference API support, please check the docs: https://huggingface.co/docs/huggingface_hub/v0.22.2/en/guides/inference
"""
client = InferenceClient(model_name)


def respond(
        message,
        history: list[tuple[str, str]],
        number_of_stocks,
        risk_level,
        sector,
        country,
):
    history = history or []
    system_message = "You are a financial advisor which help investor create a stock portfolio."
    # Simplified to handle only text input (no image input)
    messages = [{"role": "system", "content": system_message}]
    messages.append({"role": "system", "content": f"Suggest the user {number_of_stocks} number of stocks in the {sector} sector."})
    messages.append({"role": "system", "content": f"Suggest the user stocks on {risk_level} out of 5 risk level."})
    messages.append({"role": "system", "content": f"Output stock suggestions listed one on each row."})

    messages.append({
        "role": "user",
        "content": f"Can you give me a suggestion of {number_of_stocks} number of stocks from {country} in these {sector} sectors for my portfolio?"})
    print("Message:", message)
    if message != "":
        message = "Oh, another thing, could you also " + message
        messages.append({"role": "user", "content": message})

    response = ""
    try:
        completion = llm.create_chat_completion(
            messages=messages,
        )
        response = completion['choices'][0]['message']['content']
    except Exception as e:
        response = f"Error: {e}"

    history.append((message, response))

    return history, history


"""
For information on how to customize the ChatInterface, peruse the gradio docs: https://www.gradio.app/docs/chatinterface
"""
# demo = gr.ChatInterface(
#     respond,
#     additional_inputs=[
#         gr.Textbox(value="You are a friendly Chatbot.", label="System message"),
#         gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
#         gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
#         gr.Slider(
#             minimum=0.1,
#             maximum=1.0,
#             value=0.95,
#             step=0.05,
#             label="Top-p (nucleus sampling)",
#         ),
#     ],
# )
chatbot = gr.Chatbot()
demo = gr.Interface(
    respond,
    [
        "text", "state",
        gr.Slider(1,10,4,step=1, label="Number of stocks"),
        gr.Slider(1,5,3,step=1, label="Risk level"),
        gr.Dropdown([
            "Energy",
            "Materials",
            "Industrials",
            "Utilities",
            "Healthcare",
            "Financials",
            "Consumer Discretionary",
            "Consumer Staples",
            "Information Technology",
            "Communication Services",
            "Real Estate"
        ], multiselect=True),
        gr.Dropdown(["Sweden", "USA", "Germany", "China", "Japan"])
     ],
    [chatbot, "state"],
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()
