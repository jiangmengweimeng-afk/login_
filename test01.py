import pandas as pd

data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [22, 23, 21],
    'city': ['Taizhou', 'Zhoushan', 'Hangzhou']
}

df = pd.DataFrame(data)

print(df)