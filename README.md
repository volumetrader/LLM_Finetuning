---
title: Iris
emoji: 💬
colorFrom: yellow
colorTo: purple
sdk: gradio
sdk_version: 5.0.1
app_file: app.py
pinned: false
license: apache-2.0
---
This project was created as part of a course on Scalable ML ID2223 @ KTH

Purpose 
---
The purpose of this project was to fine-tune a LLM and build and inference pipeline and interface. 
We built a interface for the tasks of choosing stocks for your portfolio. You can with our tool input your risk tolerance,
markets and sectors you're interested in and our model will help suggest
personalized investment opportunities.

The base models we used for fine-tuning:
--- 
"unsloth/Llama-3.2-1B-Instruct-bnb-4bit"

"unsloth/Llama-3.2-1B-Instruct"

Datasets
---
"mlabonne/FineTome-100k"

"gbharti/finance-alpaca"


Improvement - model centric approach:
---
To improve on the performance of the model a full fine-tuning of the model could have been done instead of the lora model which is more efficient to train and requires less ram but does not have as high performance as a full fine-tuning.

Improvement - data centric approach:
---
To improve on the initial model a dataset which is more suited for our objective as a financial adivisor could boost the models performance
by receiving more domain-specific knowledge during the fine-tuning.
We found a dataset to that end with: https://huggingface.co/datasets/gbharti/finance-alpaca which we have used to train the second iteration of
our financial advisor.
