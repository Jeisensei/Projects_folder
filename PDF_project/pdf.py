from PyPDF2 import PdfReader
import re
import requests
import deepl

def extract_info_from_pdf(pdf_path):
  """
    Extracts information from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        tuple: A tuple containing the extracted information. The tuple contains the following elements:
            - name (str): The name extracted from the PDF.
            - times (str): The times extracted from the PDF.
            - start (str): The start date extracted from the PDF.
            - end (str): The end date extracted from the PDF.
            - teacher (str): The teacher's name extracted from the PDF.
            - number_of_lessons (str): The number of lessons extracted from the PDF.
            - course_type (str): The course type extracted from the PDF.
            - issue (str): The issue extracted from the PDF.
            - online (str): The online status extracted from the PDF.

    Raises:
        None

    Notes:
        - The function uses the PyPDF2 library to read the PDF file and extract the text.
        - The function uses regular expressions to search for specific patterns in the text and extract the desired information.
        - The extracted information is returned as a tuple.
  """
  reader = PdfReader("test.pdf")
  page = reader.pages[0]
  text = page.extract_text()

  name_pattern = r"作成日([\u3040-\u309F\u30A0-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF0-9A-Za-z]+\s[\u3040-\u309F\u30A0-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF0-9A-Za-z]+)"
  name_matches = re.search(name_pattern, text)
  name = name_matches[0][3:]
  # print(name)

  times_pattern = r"(週[0-9]日) 頻度" 
  times_matches = re.search(times_pattern, text)
  times = times_matches[1][:3]
  # print(times)

  start_pattern = r"([0-9]{4}\/[0-9]{2}\/[0-9]{2}) 開始日"
  start_matches = re.search(start_pattern, text)
  start = start_matches[1][:-3]
  # print(start)

  end_pattern = r"([0-9]{4}\/[0-9]{2}\/[0-9]{2}) 終了日"
  end_matches = re.search(end_pattern, text)
  end = end_matches[1][:-3]
  # print(end)

  teacher_pattern = r"([一-龯ァ-ン]*＋?[一-龯ァ-ン]+講師) 講師"
  teacher_matches = re.search(teacher_pattern, text)
  teacher = teacher_matches[1][:-3]
  # print(teacher) 

  number_of_lessons_pattern = r"([0-9]+)\s実レッスン数"
  number_of_lessons_matches = re.search(number_of_lessons_pattern, text)
  number_of_lessons = number_of_lessons_matches[1]
  # print(number_of_lessons)

  course_type_pattern = r"レッスンタイププライベートレッスン ([一-龯ぁ-んァ-ン。A-Za-z 0-9\s\（\）\-\.ヵ\nー]+)受講目的様"
  course_type_matches = re.search(course_type_pattern, text)
  course_type = course_type_matches[1]
  # print(course_type)

  issue_pattern = r"お願い申し上げます。([ー \・一-龯ぁ-んァ-ン。A-Za-z 0-9\s\（\）\-\.ヵ\n]+)課題と内容"
  issue_matches = re.search(issue_pattern, text)
  issue = issue_matches[1]
  # print(issue)

  online_pattern = r"講師([一-龯ぁ-んァ-ン]+) 通学"
  online_matches = re.search(online_pattern, text)
  online = online_matches[1]
  # print(online)

  return (name, times, start, end, teacher, number_of_lessons, course_type, issue, online)

def translate_to_english(tuple):
  """
  Translates a tuple of Japanese words to English using the DeepL API.

  Parameters:
      tuple (tuple): A tuple of Japanese words.

  Returns:
      list: A list of translated English words.
  """
  deepl_api_key = "c2772beb-6386-4c47-ad0b-339f934dc7d8:fx"
  translator = deepl.Translator(deepl_api_key)
  result_list = []
  for word in tuple:
    result = translator.translate_text(word, source_lang="ja", target_lang="EN-US")
    result_list.append(result.text)
  return result_list

name, times, start, end, teacher, number_of_lessons, course_type, issue, online = translate_to_english(extract_info_from_pdf("test.pdf"))

trello_api_key = "8e53e159bfd453ff5e591331354b8d7c"
trello_api_secret = "14582dd42cec40b4db7086b417995a96146c1278af361f5e7eceb63509faa04f"
trello_api_token = "ATTA3e3708c76c5b83e6e7d33b4c67d075ee4b940e12439164fbda436f11a980595a64DB0CC0"

url = "https://api.trello.com/1/cards"

headers = {
  "Accept": "application/json"
}

query = {
  "idBoard" : "66445a09b49a5efca4266723",
  "idList": "66445a4f53669f1039084b0d",
  "key" : trello_api_key,
  "token" : trello_api_token,
  "name" : "{} (Lesson Request)".format(name),
  "desc" : "Name: {0}\nTimes: {1}\nStart: {2}\nEnd: {3}\nTeacher: {4}\nNumber of lessons: {5}\nCourse type: {6}\nIssue: {7}\nOnline: {8}".format(name, times, start, end, teacher, number_of_lessons, course_type, issue, online)
}

response = requests.request(
   "POST",
   url,
   headers=headers,
   params=query
)

print(name, times, start, end, teacher, number_of_lessons, course_type, issue, online)