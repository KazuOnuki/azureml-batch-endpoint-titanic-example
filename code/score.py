# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import numpy as np
import pandas as pd
import joblib
from logging import getLogger # 途中で誤ってloggingを汚さないように個別にimport

def init():
  global model
  # This name is model.id of model that we want to deploy deserialize the model file back
  model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.pkl')
  try:
      print(f'Loading model from path ({model_path}).')
      model = joblib.load(model_path)
      print("Loading successful.")
  except Exception as e:
      print(f'error:{e}')
      raise

def run(mini_batch):
  '''
  predict function

  Parameters
  ------
  mini_batch: List
    input file(.csv) list
  
  Returns
  ------
  resultList: List
  '''
  print(f"run method start: {__file__}, run({mini_batch})")
  resultList = []

  for file in mini_batch:
    df = pd.read_csv(file)
    print("*"*100)
    print(df)
    try:
      result = model.predict(df)
      print(f'result: {result}')
      resultList.append(
        f'Files: {os.path.basename(file)}--Results:{result.tolist()}'
      )
    except Exception as e:
      print(f'error: {e}')
    print("*"*100)

  return resultList
