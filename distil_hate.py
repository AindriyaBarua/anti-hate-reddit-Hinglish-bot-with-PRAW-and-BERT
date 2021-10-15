from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

def read_data(path):
  dataset_df = pd.read_excel(path, dtype=object)
  print(dataset_df)
  return dataset_df

dataset_df = read_data('codemix-hin-hate.xlsx')

dataset_df = dataset_df[dataset_df['label'].notna()]
print(dataset_df)

train_df, eval_df= train_test_split(dataset_df, test_size=0.20, random_state=42)

model_args = ClassificationArgs(num_train_epochs=1)

model = ClassificationModel(
    "distilbert", "distilbert-base-uncased", args=model_args, use_cuda = False
)

model.train_model(train_df)

result, model_outputs, wrong_predictions = model.eval_model(eval_df)

print(result, model_outputs, wrong_predictions)

import pickle
pickle.dump(model, open("distill_model" + '.pkl', 'wb'))