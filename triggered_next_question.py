"""triggered_next_question.ipynb
Author:Rutuja Papade
Date:21-02-2024
Original file is located at
    https://colab.research.google.com/drive/1lLXPUPpVDGyJjXHNg_S-JIs4_U9W_ajp
Used: triggered_next_question
"""
from intent_analysis import question_ans_analysis
import pandas as pd

def triggred_questions(input_data,input_id):

    result = question_ans_analysis(input_data,input_id)

    if result['existing_home_loan'] is None:
        response = "Do you have any existing home loan?"
    elif result['bank_name_token'] is None:
        response = "Can you please tell me from which bank you have taken the home loan?"
    elif result['more_details_token'] is None:
        response = " Sir, can you please help me with a few more details for sharing the exact offer details?"
    elif result['sanction_amt_token'] is None:
        response = "What is your home loan sanction amount?"
    elif result['emi_amt_token'] is None:
        response = "What is the EMI that you are paying?"
    elif result['outstanding_amt_token'] is None:
        response = "What is your outstanding amount?"
    elif result['obligation_token'] is None:
        response = "Do you have any Other Obligation like Personal loan or car loan?"
    elif result['appointment_details'] is None:
        response = "Thank you Sir for your input, can you give me few minutes so that I can come up with and offer for you? " \
                   "You are qualifying for a Preapproved Home Loan Balance Transfer offer of <#var>. Please let us know of a " \
                   "suitable day and time for scheduling your appointment with our sales manager"
    else:
        response = "Thank you for your valuable time, have a nice day ahead."

    return response
