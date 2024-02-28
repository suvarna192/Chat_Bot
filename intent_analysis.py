"""intent_analysis.ipynb
Author:Rutuja Papade
Date:21-02-2024
Original file is located at
    https://colab.research.google.com/drive/1lLXPUPpVDGyJjXHNg_S-JIs4_U9W_ajp
Used: analyse the intent and find the token from it
"""
import re

from span_marker import SpanMarkerModel
model = SpanMarkerModel.from_pretrained("tomaarsen/span-marker-bert-base-uncased-cross-ner")
from nltk.tokenize import sent_tokenize
from spacy.lang.en import English
nlp = English()  # just the language with no pipeline


def question_ans_analysis(ques_ans_string,input_id):

   def find_type(words, input_sentence):
       sentences = sent_tokenize(input_sentence)
       result_tokens = []

       for target_word in words:
           for i, sent in enumerate(sentences):
               if target_word.lower() in sent.lower():

                   if i + 1 < len(sentences):
                       combined_sentence = sent + ' ' + sentences[i + 1]
                       result_tokens.append(combined_sentence)
                   else:

                       result_tokens.append(sent)


       token = " ".join(result_tokens)


       return token



   def find_bank_name(input_bank_name_sentence):
       if input_bank_name_sentence:
           cleaned_sentence = re.sub(r'[^A-Za-z0-9]+', ' ', input_bank_name_sentence)

           # make example sentence

           entities = model.predict(str(cleaned_sentence))

           for entity in entities:
               if entity['label'] == "organisation":
                   bank_name = entity['span']
                   return bank_name


   def find_number(input_sentence):
       if input_sentence:
           number_pattern = r'\b\d+(?:\.\d+)?\b'
           numbers = re.findall(number_pattern, input_sentence)

           unique_num = set(numbers)
       else:
           unique_num = None

       return unique_num if unique_num else None

   def yes_no(input_sentence):

       if input_sentence:
           yes_no_phrases = [
               r"yes",
               r"I have",
               r"don't",
               r"do not",
               r"dont"
           ]

           yes_no_pattern = "|".join(yes_no_phrases)
           matches = re.findall(yes_no_pattern, input_sentence , re.IGNORECASE)

       else:
           matches = None

       return matches if matches else None

   def yes_okay(input_sentence):

       if input_sentence:
           yes_no_phrases = [
               r"yes",
               r"okay",
               r"I have",
               r"yeah"
           ]

           yes_no_pattern = "|".join(yes_no_phrases)
           matches = re.findall(yes_no_pattern, input_sentence , re.IGNORECASE)

           return matches

   def detect_days_time(input_sentence):

       if input_sentence:
           # Regular expressions to match days of the week and time in AM/PM format
           days_pattern = r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|tomorrow|day after tomorrow)\b'
           time_pattern = r'\b(?:[0-9]|0[0-9]|1[0-2])(?::[0-5][0-9])?\s*(?:am|pm|a\.m\.|p\.m\.)\b'

           # Find all matches of days of the week
           days_matches = re.findall(days_pattern, input_sentence, flags=re.IGNORECASE)

           # Find all matches of time in AM/PM format
           time_matches = re.findall(time_pattern, input_sentence, flags=re.IGNORECASE)

           result_day_time = days_matches + time_matches

           return result_day_time


   #existing home laon
   list_words = ["existing home loan"]
   existing_home_loan_sentence = find_type(list_words, ques_ans_string)
   existing_home_loan_token = yes_okay(existing_home_loan_sentence)


   #bank name
   list_words = ["which bank", "bank name","loan from","loan in"]
   bank_name_sentence = find_type(list_words, ques_ans_string)
   # print("bank_name_sentence",bank_name_sentence)
   bank_name_token = find_bank_name(bank_name_sentence)

   #interested in more details
   list_words = ["help me with a few more details"]
   more_details_sentence = find_type(list_words, ques_ans_string)
   more_details_token = yes_okay(more_details_sentence)

   #sanction amount
   list_words = ["sanction amount", "taken"]
   sanction_amt_sentence = find_type(list_words, ques_ans_string)
   sanction_amt_token = find_number(sanction_amt_sentence)

   #emi amount
   list_words = ["emi"]
   emi_amt_sentence = find_type(list_words, ques_ans_string)
   emi_amt_token = find_number(emi_amt_sentence)

   #outstanding amount
   list_words = ["outstanding amount", "remaining","left"]
   outstanding_amt_sentence = find_type(list_words, ques_ans_string)
   outstanding_amt_token = find_number(outstanding_amt_sentence)

   #obligations
   list_words = ["Obligation"]
   obligation_sentence = find_type(list_words, ques_ans_string)
   obligation_token = yes_no(obligation_sentence)

   # appointment details
   list_words = ["appointment"]
   app_details_sentence = find_type(list_words, ques_ans_string)
   app_details_token = detect_days_time(app_details_sentence)

   data = {"input_id": str(input_id),
       "existing_home_loan": existing_home_loan_token,
       "bank_name_token": bank_name_token,
       "more_details_token":more_details_token,
       "sanction_amt_token":sanction_amt_token,
       "emi_amt_token":emi_amt_token,
       "outstanding_amt_token":outstanding_amt_token,
       "obligation_token":obligation_token,
       "appointment_details": app_details_token
   }

   return data

