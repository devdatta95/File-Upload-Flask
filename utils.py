import pandas as pd
from config import *
import numpy as np

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_data(file_path):
    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    df.dropna(inplace=True)
    df['Random Column'] = np.random.randint(0, 1000, len(df))
    df.drop_duplicates(inplace=True)
    df = df[(df['Random Column'] > 50) & (df['Random Column'] < 800)]
    df["Addr"] = "Mumbai_Andheri"

    df = df.head(10)
    output_path = file_path.rsplit('.', 1)[0] + '_preprocessed.csv'
    df.to_csv(output_path, index=False)

    return output_path
