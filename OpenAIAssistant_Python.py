"""
This module is for running an OpenAI assistant using Python. 
The purpose of creating this module is to facilitate the difficulty in navigating how to 
use an OpenAI assistant in an applicant instantly. 

Make sure the have your OpenAI API key and Assistant ID ready. 

Date: 4/26/2024
Author: Hamid Rezaee (@iamhamidrezaee)
"""

import openai

# Enter the API key and assistant ID 
openai.api_key = "YOUR_API_KEY"
assistant_id = "YOUR_ASSISTANT_ID"

def create_thread(prompt):
    """
    Creates a thread and run object
    
    params:
        assistant_id (string): The OpenAI assistant ID available on the OpenAI assistant dashboard prompt

    returns: run ID and thread ID as strings
    """

    # Create a thread
    thread = openai.beta.threads.create()
    my_thread_id = thread.id

    # Create a message
    message = openai.beta.threads.messages.create(
        thread_id=my_thread_id,
        role="user",
        content=prompt
    )
    # Create the run object
    run = openai.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=assistant_id,
    ) 
    return run.id, thread.id

def check_status(run_id,thread_id):
    """
    Checks the status of run and whehter is queued, canceled, in progress, or other status

    params:
        run_id (string): The run ID received from create_thread
        thread_id (string): The thread ID received from create_thread

    returns: run status 
    """

    run = openai.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status


def return_response(prompt):
    """
    Takes a prompt and returns the response from the assistant

    params:
        prompt (string): The prompt passed by the user to the assistant
    
    returns: The response that comes from the OpenAI assistant a string
    """

    assistant_id = "YOUR_ASSISTANT_ID"

    my_run_id, my_thread_id = create_thread(assistant_id, prompt)
    status = check_status(my_run_id,my_thread_id)
    while (status != "completed"):
        status = check_status(my_run_id,my_thread_id)
    response = openai.beta.threads.messages.list(
    thread_id=my_thread_id
    )
    if response.data:
        return response.data[0].content[0].text.value