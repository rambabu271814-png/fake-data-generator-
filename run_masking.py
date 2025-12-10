from fake_data_generator import mask_dataframe
import pandas as pd

INPUT_PATH = r"C:\Users\Administrator\Downloads\generate_fake_data.csv"
OUTPUT_PATH = r"C:\Users\rss005\Downloads\generate_fake_data_masked.csv"

df = pd.read_csv(INPUT_PATH, dtype=str)
masked_df = mask_dataframe(df)
masked_df.to_csv(OUTPUT_PATH, index=False)

print("Saved masked file to:", OUTPUT_PATH)
