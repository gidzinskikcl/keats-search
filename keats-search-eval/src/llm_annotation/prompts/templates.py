from abc import ABC

class PromptTemplate(ABC):
    pass


class V1(PromptTemplate):
    VARIANT = "v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a domain expert in the subject area of {course_name}.
    You are assisting in the evaluation of search engine results.
    Given a user query and a document retrieved from lecture "{lecture_name}", your task is to determine whether the document actually answers the query or merely introduces or hints at the topic.
    Your goal is to distinguish between relevant content that addresses the user's question directly and content that does not provide a meaningful or complete answer.
    """

    USER_PROMPT_TEMPLATE = """
    Follow these steps
    1. Read the question: {question}
    2. Read the potential answer to this question: {answer} 
    3. Determine whether the answer directly and sufficiently answers the question. Do not mark it as relevant if it only introduces the topic or partially leads up to an answer.
    4. Present your output using the following format:
        - question 
        - answer
        - relevance: relevant | not relevant

    Here is an example of a relevant answer:
    
    Input:
        - question: Why alter a code pointer in code injection?
        - answer: Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow.
     
    Output:
        - question: Why alter a code pointer in code injection?
        - answer: Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow.
        - relevance: relevant

    Here is an example of a not relevant answer:
    
    Input:
        - question: Why alter a code pointer in code injection?
        - answer: Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow.
     
    Output:
        - question: Why alter a code pointer in code injection?
        - answer: Code injection techniques are often used to improve software performance by optimizing memory access patterns.
        - relevance: not relevant
    """

class V2(PromptTemplate):
    VARIANT = "v2"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a domain expert in the subject area of {course_name}.
    You are assisting in the evaluation of search engine results.
    Given a user query and a document retrieved from lecture "{lecture_name}", your task is to determine whether the document answers the query or not.
    Your goal is to distinguish between relevant content that addresses the user's question directly and content that does not provide a meaningful or complete answer.
    """

    USER_PROMPT_TEMPLATE = """
    Follow these steps
    1. Read the question: {question}
    2. Read the potential answer to this question: {answer} 
    3. Determine whether the answer directly and sufficiently answers the question. Do not mark it as relevant if it only introduces the topic.
    4. Present your output using the following format:
        - question 
        - answer
        - relevance: relevant | not relevant

    Here is an example of a relevant answer:
    
    Input:
        - question: Why alter a code pointer in code injection?
        - answer: Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow.
     
    Output:
        - question: Why alter a code pointer in code injection?
        - answer: Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow.
        - relevance: relevant

    Here is an example of a not relevant answer:
    
    Input:
        - question: Why alter a code pointer in code injection?
        - answer: Code injection techniques are often used to improve software performance by optimizing memory access patterns.
     
    Output:
        - question: Why alter a code pointer in code injection?
        - answer: Code injection techniques are often used to improve software performance by optimizing memory access patterns.
        - relevance: not relevant
    """

class V3(PromptTemplate):
    VARIANT = "v3"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a domain expert in the subject area of {course_name}.
    You are assisting in the evaluation of search engine results.
    Given a user query and a document retrieved from lecture "{lecture_name}", your task is to determine whether the document actually answers the query or merely introduces or hints at the topic.
    Your goal is to distinguish between relevant content that addresses the user's question directly and content that does not provide a meaningful or complete answer.
    """

    USER_PROMPT_TEMPLATE = """
    Follow these steps
    1. Read the question: {question}
    2. Read the potential answer to this question: {answer} 
    3. Determine whether the answer directly and sufficiently answers the question. Do not mark it as relevant if it only introduces the topic or partially leads up to an answer.
    4. Present your output using the following format:
        - question 
        - answer
        - relevance: relevant | not relevant

    Here is an example of a relevant answer:
    
    Input:
        - question: Why alter a code pointer in code injection?
        - answer: Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow.
     
    Output:
        - question: Why alter a code pointer in code injection?
        - answer: Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow.
        - relevance: relevant

    Here is an example of a not relevant answer:
    
    Input:
        - question: Why alter a code pointer in code injection?
        - answer: Code injection techniques are often used to improve software performance by optimizing memory access patterns.
     
    Output:
        - question: Why alter a code pointer in code injection?
        - answer: Code injection techniques are often used to improve software performance by optimizing memory access patterns.
        - relevance: not relevant
    """