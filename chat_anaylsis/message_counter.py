import pandas as pd

# Date format: yy-mm-dd
# 월별, 날짜별, 시간대 별

chat_df = pd.read_csv("./data/kakaochat_cleaning.csv")
chat_df['date'] = pd.to_datetime(chat_df['date'], format='%y-%m-%d')
chat_df['year'] = chat_df['date'].dt.year
chat_df['month'] = chat_df['date'].dt.month

yearly_messages = chat_df.groupby(chat_df['date'].dt.year).size().reset_index(name='message_count')
yearly_by_monthly_messages = chat_df.groupby(['year', 'month']).size().reset_index(name='message_count')
daily_messages = chat_df.groupby('date').size().reset_index(name='message_count')
day_of_week_messages = chat_df.groupby('dayname').size().reset_index(name='message_count')

yearly_messages.to_csv('./data/yearly_messages.csv', index=False)
yearly_by_monthly_messages.to_csv('./data/yearly_by_monthly_message.csv', index=False)
daily_messages.to_csv('./data/daily_messages.csv', index=False)
day_of_week_messages.to_csv('./data/day_of_week_message.csv', index=False)

# Add hours
chat_df['date'] = pd.to_datetime(chat_df['date'].dt.date.astype(str) + ' ' + chat_df['time'].str[:2] + ':00', format='%Y-%m-%d %H:%M')
hourly_messages = chat_df.groupby(chat_df['date'].dt.hour).size().reset_index(name='message_count')
hourly_messages.to_csv('./data/hourly_messages.csv', index=False)