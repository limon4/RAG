import os

import pandas as pd

prev_directory = os.path.dirname(os.getcwd())

df = pd.read_csv(
            fr"{prev_directory}\resources\expanded_questions_aux.csv",
            usecols=['original', 'expandida']
        )

print(len(df['original'].unique()))