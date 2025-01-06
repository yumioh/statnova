import pandas as pd

chat_df = pd.read_csv("./chat_anaylsis/data/chat_noun_tagging.csv")

keyword = "과목"

# filtered_df = chat_df[chat_df['noun_token'].apply(lambda x: any(k in x for k in keywords))]

filtered_df = chat_df[chat_df['noun_token'].apply(lambda x: keyword in x)]

print(filtered_df.head())

filtered_df.to_csv(f"./chat_anaylsis/data/{keyword}_export.csv")
