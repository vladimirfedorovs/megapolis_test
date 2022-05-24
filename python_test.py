import pandas as pd
import requests as rq
import json

req_post = rq.get('http://jsonplaceholder.typicode.com/posts') # выгружаем посты
req_com = rq.get('http://jsonplaceholder.typicode.com/comments') # выгружаем комменты

posts = json.loads(req_post.content)  # декодируем посты
comments = json.loads(req_com.content)  # декодируем комменты

df_post = pd.json_normalize(posts) # преобразуем json в pandas dataframe
df_comments = pd.json_normalize(comments)  #преобразуем json в pandas dataframe

df_gb_com = df_comments.groupby(by = ['postId'], as_index = True).count() # считаем количество комментариев у каждого поста
df_gb_post = df_post.groupby(by = ['userId'],as_index = True).count() # считаем количество постов у каждого пользователя

df_merge = df_post[['userId','id']].merge(df_gb_com['id'], how = 'left', left_on='id', right_on='postId') # джойним количество комментариев к каждому посту с таблицей постов
df_merge = df_merge[['userId','id_y']].groupby(by = ['userId']).sum() # считаем сумму комментариев для каждого пользователя

df_merge = df_merge.merge(df_gb_post['id'], how = 'left', left_on='userId', right_on='userId') # собираем итоговый dataframe
df_merge['average_comments_per_post'] = df_merge['id_y']/df_merge['id'] # добавляем среднее число постов для каждого пользователя
print(df_merge['average_comments_per_post'].to_dict()) # выводим словарь
