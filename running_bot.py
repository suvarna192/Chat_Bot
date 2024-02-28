import nltk
import re
import random
import pandas as pd
from triggered_next_question import triggred_questions

# Define function to respond to user input
def respond(user_input,input_id):
    responses = triggred_questions(user_input,input_id)
    return responses

def running_bot(user_input, input_id):
    # Load existing data from Excel file
    try:
        existing_dataframe = pd.read_excel('./Testing.xlsx', sheet_name='AKER')
    except FileNotFoundError:
        # Create a new DataFrame if the file doesn't exist
        existing_dataframe = pd.DataFrame(columns=['call_id', 'user_input', 'bot'])

    filtered_df = existing_dataframe[existing_dataframe['call_id'].astype(str) == input_id]
    greeting_triggered = filtered_df['bot'].str.contains('good morning', case=False).any()
    topup_triggered = filtered_df['bot'].str.contains('you can get a High Topup of value', case=False).any()

    save_chat_history = []

    save_chat_history.append(user_input)

    positive_response = ["okay", "yes", "interested", "yeah", "sure", "ok"]
    negative_response = ['quit', 'exit', 'bye', "not interested", "i don't want to talk to you",
                         "end the call", "thank you", "call me later", "busy", "who are you", "later", "no"]

    if any(word in user_input for word in ["rate of interest", "interest rate", "rate interest"]):
        chat_hist = "Rate of interest depends on multiple factors; In case you are interested, based on your eligibility," \
                    " our authorized sales representative will get in touch with you to discuss the rate of interest."

    elif any(word in user_input for word in ["Previously I had taken a home loan", "status", "previous loan"]):
        chat_hist = "Yes, certainly. Can you please help me with a few details and I can help you better with your Pre-approved Home Loan balance transfer Offer."

    elif any(word in user_input for word in ["loan applications", "How long it will take for loan applications to get processed", "process", "application"]):
        chat_hist = "Your loan application will get approved within 48 hours post document submission. Our sales representative will get in touch with you shortly to help you with the list of documents."

    elif not greeting_triggered and any(word in user_input for word in ["hi", "hello", "gm", "good morning"]):
        chat_hist = "Good morning, Mr. John, this is Bajajbot. I am calling on behalf of Bajaj Housing Finance. Since you are a valuable Customer to Bajaj, we have a Pre-Approved Home Loan - Balance Transfer offer of 12 lacs."
        # Set greeting_triggered to True
        greeting_triggered = True


    elif greeting_triggered and not topup_triggered and any(word in user_input for word in positive_response):
        chat_hist = "By availing this Offer, you can get a High Topup of value upto with maximum savings in EMI. " \
                    "Are you interested in this Offer?"

    elif any(word in user_input for word in negative_response):
        chat_hist = "Thank you for your valuable time, have a nice day ahead."

    elif topup_triggered:
        combined_series = filtered_df.apply(lambda row: f"{row['user_input']} {row['bot']}", axis=1)
        # Step 2: Join all combined row values into one string
        combined_messages = '. '.join(combined_series)
        my_string = combined_messages + " " + user_input
        chat_hist = respond(my_string,str(input_id))

    else:
        chat_hist = "Please give the valid response"

    # New entry to add
    new_entry = {
        "call_id": input_id,
        "user_input": user_input,
        "bot": chat_hist
    }

    # Append the new entry to the existing DataFrame
    existing_dataframe = existing_dataframe._append(new_entry, ignore_index=True)

    # Save the DataFrame to the Excel file
    with pd.ExcelWriter('./Testing.xlsx', engine='xlsxwriter') as writer:
        existing_dataframe.to_excel(writer, sheet_name='AKER', index=False)

    return chat_hist
