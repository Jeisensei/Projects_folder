from PyPDF2 import PdfReader
import deepl
import sys
import os

deepl_api_key = "c2772beb-6386-4c47-ad0b-339f934dc7d8:fx"

def extract_info_from_pdf(pdf_path):
  reader = PdfReader(pdf_path)
  page = reader.pages[0]
  print(page)
  text = page.extract_text(extraction_mode="layout")
  print(text)

  return (text)

def translate_to_english(tuple):
  """
  Translates a tuple of Japanese words to English using the DeepL API.

  Parameters:
      tuple (tuple): A tuple of Japanese words.

  Returns:
      list: A list of translated English words.
  """
  translator = deepl.Translator(deepl_api_key)
  result_list = []
  for word in tuple:
    result = translator.translate_text(word, source_lang="ja", target_lang="EN-US")
    result_list.append(result.text)
  return result_list

location = "".join([str(os.getcwd()), "/",  sys.argv[1]])
print(location)

extract_info_from_pdf(location)


