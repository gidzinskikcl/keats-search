from abc import ABC

class PromptTemplate(ABC):
    VARIANT = ""

class V1(PromptTemplate):
    VARIANT = "minimum-v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a domain expert in {course_name}. Your task is to evaluate whether a document retrieved from lecture "{lecture_name}" answers a student's question.
    """

    USER_PROMPT_TEMPLATE = """
    Question: {question}

    Answer: {answer}

    Is the answer relevant to the question?

    - "relevant" means it clearly and completely answers the question.
    - "notrelevant" means it is off-topic, vague, or incomplete.

    Provide your output in this format:
    - relevance: "relevant" | "notrelevant"
    """


class V2(PromptTemplate):
    VARIANT = "basic-v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a domain expert in the subject area of {course_name}. Your task is to evaluate whether a document retrieved from the lecture "{lecture_name}" directly and sufficiently answers a user's query.
    """

    USER_PROMPT_TEMPLATE = """
    1. Read the question: {question}
    2. Read the document content: {answer} 
    3. Decide whether the answer directly and sufficiently addresses the question.
        - "relevant" means the document clearly and fully addresses the question.
        - "notrelevant" means it is off-topic, incomplete, or vague.
    4. Provide your answer in this format:
        - question: <repeat the question>
        - answer: <repeat the document content>
        - relevance: "relevant" | "notrelevant"
    """


class V3(PromptTemplate):
    VARIANT = "F2-v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a domain expert in the subject area of {course_name}. Your task is to evaluate whether a document retrieved from the lecture "{lecture_name}" directly and sufficiently answers a user's query.
    """

    USER_PROMPT_TEMPLATE = """
    1. Read the question: {question}
    2. Read the document content: {answer} 
    3. Decide whether the answer directly and sufficiently addresses the question.
        - "relevant" means the document clearly and fully addresses the question.
        - "notrelevant" means it is off-topic, incomplete, or vague.
    4. Provide your answer in this format:
        - question: <repeat the question>
        - answer: <repeat the document content>
        - relevance: "relevant" | "notrelevant"
    
    Examples:

    Example 1:
    question: "Why alter a code pointer in code injection?"
    answer: "Altering a code pointer, such as a return address or function pointer, allows an attacker to redirect the program’s execution to malicious code. This is a key step in hijacking control flow during code injection attacks."
    relevance: "relevant"

    Example 2:
    question: "What are the benefits of virtual memory?"
    answer: "Code injection allows you to hijack execution by modifying return addresses."
    relevance: "notrelevant"

    Now, based on the above guidelines and examples, provide your own evaluation in the same format.
    """


class V4(PromptTemplate):
    VARIANT = "F4-v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a domain expert in the subject area of {course_name}. Your task is to evaluate whether a document retrieved from the lecture "{lecture_name}" directly and sufficiently answers a user's query.
    """

    USER_PROMPT_TEMPLATE = """
    1. Read the question: {question}
    2. Read the document content: {answer} 
    3. Decide whether the answer directly and sufficiently addresses the question.
        - "relevant" means the document clearly and fully addresses the question.
        - "notrelevant" means it is off-topic, incomplete, or vague.
    4. Provide your answer in this format:
        - question: <repeat the question>
        - answer: <repeat the document content>
        - relevance: "relevant" | "notrelevant"

    Examples:

    Example 1:
    question: "Why alter a code pointer in code injection?"
    answer: "Altering a code pointer, such as a return address or function pointer, allows an attacker to redirect the program’s execution to malicious code. This is a key step in hijacking control flow during code injection attacks."
    relevance: "relevant"

    Example 2:
    question: "What are the benefits of virtual memory?"
    answer: "Code injection allows you to hijack execution by modifying return addresses."
    relevance: "notrelevant"

    Example 3:
    question: "What are the advantages and disadvantages of multiple inheritance?"
    answer: "Multiple inheritance enables a class to combine and extend functionalities from multiple parent classes, promoting flexible and modular design; however, it can introduce ambiguity in method resolution, increased coupling, and maintenance challenges."
    relevance: "relevant"

    Example 4:
    question: "What is dynamic programming?"
    answer: "Dynamic programming is commonly used in bioinformatics to solve sequence alignment problems."
    relevance: "notrelevant"

    Now, based on the above guidelines and examples, provide your own evaluation in the same format.
    """

class V5(PromptTemplate):
    """
    - modify how to decide relevance - it can be lengthy, hard but still it can be relevant 
    - added definition for relevance (def)
    """
    VARIANT = "def-F2-v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are an expert in the subject of {course_name}. Your job is to decide whether a document retrieved from the lecture "{lecture_name}" directly and sufficiently answers a student's query.
    """

    USER_PROMPT_TEMPLATE = """
    Follow these steps:
    
    1. Read the question: {question}
    2. Read the document content: {answer}
    3. Decide whether the answer directly and sufficiently addresses the question.

    Definitions:
    - "relevant": The answer clearly or thoroughly addresses the question — even if the explanation is technical, lengthy, or difficult to follow.
    - "notrelevant": The answer is incomplete, off-topic, vague, or only loosely related to the question.

    Respond using this format:
    - question: <repeat the question>
    - answer: <repeat the document content>
    - relevance: "relevant" | "notrelevant"

    Examples:

    Example 1 (relevant):
    question: "Why alter a code pointer in code injection?"
    answer: "Altering a code pointer, such as a return address or function pointer, allows an attacker to redirect the program’s execution to malicious code. This is a key step in hijacking control flow during code injection attacks."
    relevance: "relevant"

    Example 2 (notrelevant):
    question: "What are the benefits of virtual memory?"
    answer: "Code injection allows you to hijack execution by modifying return addresses."
    relevance: "notrelevant"

    Now, provide your evaluation in the same format.
    """

class V6(PromptTemplate):
    """
    - modify how to decide relevance - it can be lengthy, hard but still it can be relevant 
    - added definition for relevance (def)
    - add partial relevance example (F3)
    """
    VARIANT = "def-F3-v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are an expert in the subject of {course_name}. Your job is to decide whether a document retrieved from the lecture "{lecture_name}" directly and sufficiently answers a student's query.
    """

    USER_PROMPT_TEMPLATE = """
    Follow these steps:
    
    1. Read the question: {question}
    2. Read the document content: {answer}
    3. Decide whether the answer directly and sufficiently addresses the question.

    Definitions:
    - "relevant": The answer clearly or thoroughly addresses the question — even if the explanation is technical, lengthy, or difficult to follow.
    - "notrelevant": The answer is incomplete, off-topic, vague, or only loosely related to the question.

    Respond using this format:
    - question: <repeat the question>
    - answer: <repeat the document content>
    - relevance: "relevant" | "notrelevant"

    Examples:

    Example 1 (relevant):
    question: "Why alter a code pointer in code injection?"
    answer: "Altering a code pointer, such as a return address or function pointer, allows an attacker to redirect the program’s execution to malicious code. This is a key step in hijacking control flow during code injection attacks."
    relevance: "relevant"

    Example 2 (notrelevant):
    question: "What are the benefits of virtual memory?"
    answer: "Code injection allows you to hijack execution by modifying return addresses."
    relevance: "notrelevant"

    Example 3 (notrelevant - partial match):
    question: "How does a memory page fault occur?"
    answer: "Virtual memory allows programs to use more memory than is physically available."
    relevance: "notrelevant"

    Now, provide your evaluation in the same format.
    """

class V7(PromptTemplate):
    """
    - modify how to decide relevance - it can be length, hard but still relevant 
    - added definition for relevance (def)
    - add reasoning (COT)
    """
    VARIANT = "def-F2-COT-v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are an expert in the subject of {course_name}. Your job is to decide whether a document retrieved from the lecture "{lecture_name}" directly and sufficiently answers a student's query.
    """

    USER_PROMPT_TEMPLATE = """
    Follow these steps:
    
    1. Read the question: {question}
    2. Read the document content: {answer}
    3. Decide whether the answer directly and sufficiently addresses the question. If not, explain what’s missing or off-topic in your reasoning.

    Definitions:
    - "relevant": The answer clearly or thoroughly addresses the question — even if the explanation is technical, lengthy, or difficult to follow.
    - "notrelevant": The answer is incomplete, off-topic, vague, or only loosely related to the question.

    Respond using this format:
    - question: <repeat the question>
    - answer: <repeat the document content>
    - relevance: "relevant" | "notrelevant"
    - reasoning: <brief explanation of your decision>

    Examples:

    Example 1 (relevant):
    question: "Why alter a code pointer in code injection?"
    answer: "Altering a code pointer, such as a return address or function pointer, allows an attacker to redirect the program’s execution to malicious code. This is a key step in hijacking control flow during code injection attacks."
    reasoning: This answer directly addresses the mechanism and purpose of altering code pointers in code injection.
    relevance: "relevant"

    Example 2 (notrelevant):
    question: "What are the benefits of virtual memory?"
    answer: "Code injection allows you to hijack execution by modifying return addresses."
    reasoning: The answer discusses code injection, not virtual memory or its benefits.
    relevance: "notrelevant"

    Now, provide your evaluation in the same format.
    """

class V8(PromptTemplate):
    """
    - modify how to decide relevance - it can be length, hard but still relevant 
    - added definition for relevance (def)
    - add partial relevance example (F3)
    - add reasoning (COT)
    """
    VARIANT = "def-F3-COT-v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are an expert in the subject of {course_name}. Your job is to decide whether a document retrieved from the lecture "{lecture_name}" directly and sufficiently answers a student's query.
    """

    USER_PROMPT_TEMPLATE = """
    Follow these steps:
    
    1. Read the question: {question}
    2. Read the document content: {answer}
    3. Decide whether the answer directly and sufficiently addresses the question. If not, explain what’s missing or off-topic in your reasoning.

    Definitions:
    - "relevant": The answer clearly or thoroughly addresses the question — even if the explanation is technical, lengthy, or difficult to follow.
    - "notrelevant": The answer is incomplete, off-topic, vague, or only loosely related to the question.

    Respond using this format:
    - question: <repeat the question>
    - answer: <repeat the document content>
    - relevance: "relevant" | "notrelevant"
    - reasoning: <brief explanation of your decision>

    Examples:

    Example 1 (relevant):
    question: "Why alter a code pointer in code injection?"
    answer: "Altering a code pointer, such as a return address or function pointer, allows an attacker to redirect the program’s execution to malicious code. This is a key step in hijacking control flow during code injection attacks."
    reasoning: This answer directly addresses the mechanism and purpose of altering code pointers in code injection.
    relevance: "relevant"

    Example 2 (notrelevant):
    question: "What are the benefits of virtual memory?"
    answer: "Code injection allows you to hijack execution by modifying return addresses."
    reasoning: The answer discusses code injection, not virtual memory or its benefits.
    relevance: "notrelevant"

    Example 3 (notrelevant - partial match):
    question: "How does a memory page fault occur?"
    answer: "Virtual memory allows programs to use more memory than is physically available."
    reasoning: While related to virtual memory, the answer doesn't explain what causes a page fault.
    relevance: "notrelevant"

    Now, provide your evaluation in the same format.
    """