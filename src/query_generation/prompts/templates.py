from abc import ABC

class PromptTemplate(ABC):
    pass


class V1(PromptTemplate):

    VARIANT = "v1"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a computer science student enrolled in the course "{course_name}".
    You have carefully studied the lecture content provided below.
    To check your understanding, generate a set of clear, relevant questions you might ask your lecturer.
    Each question should be answerable using only the lecture content.
    """

    USER_PROMPT_TEMPLATE = """
    1. Carefully read the lecture content: "{lecture_content}"

    2. Generate {num_questions} questions and answers based only on this content:
        a) Write a clear and concise question.
        b) Assign a difficulty level:
            - Basic: direct factual question (e.g., definitions, lists)
            - Intermediate: involves understanding or explaining relationships between ideas
            - Advanced: requires connecting multiple ideas, reasoning through examples, or analyzing concepts
        c) Provide a direct answer from the lecture content.

    3. For each question, present your output with the following structure:
        - question: The question text
        - label: Difficulty level (Basic/Intermediate/Advanced)
        - answer: The answer based on the lecture content.

    Here is an example:

    <lecture content>

    Anatomy of a code injection attack
    Goal of code injection. To hijack the execution of the target application/program toward some code injected by the attacker.
    Unlike overwriting the return address of a function with another return address that may result in the termination of the process by returning a segmentation fault, here we inject a malicious code (shellcode) into a writable memory region.
    How can an attacker perform code injection?
    1. Inject the code to be executed (shellcode) into a writable memory region (stack, data, heap, etc.).
    2. Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow. The return address will be the address of the writable memory region that contains the shellcode.
    To inject code, three elements (NOP sled, shellcode, and shellcode address) need to be present, which compose an injection vector.
    So – an injection vector is composed of:
    1. NOP sled (optional): a sequence of do-nothing instructions (NOP). It is used to ease the exploitation, such that the attacker can jump anywhere inside and will eventually reach the shellcode to execute it.
    2. Shellcode: a sequence of machine instructions executed as a result of a code injection attack. Typically, a shellcode executes a shell (eg, execve(“/bin/sh”)). The shellcode is injected by the attacker into a writable and executable memory region. The address of the writable memory region is called the shellcode address.
    3. Shellcode address: The address of the memory region that contains the shellcode.

    </lecture content>

    <student response>
    [
        (
            - question: "Shellcode"
            - label: Basic
            - answer: "Shellcode: a sequence of machine instructions executed as a result of a code injection attack. Typically, a shellcode executes a shell (eg, execve(“/bin/sh”)). The shellcode is injected by the attacker into a writable and executable memory region."
        ),
        (
            - question: "Shellcode address"
            - label: Basic
            - answer: "The address of the memory region that contains the shellcode."
        ),
        (
            - question: "Goal of code injection attack"
            - label: Intermediate
            - answer: "To hijack the execution of the target application/program toward some code injected by the attacker."
        ),
        (
            - question: "Why alter a code pointer in code injection?"
            - label: Intermediate
            - answer: "Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow."
        ),
        (
            - question: "Why is the NOP sled considered optional in a code injection vector?"
            - label: Advanced
            - answer: "NOP sled (optional): a sequence of do-nothing instructions (NOP). It is used to ease the exploitation, such that the attacker can jump anywhere inside and will eventually reach the shellcode to execute it."
        ),
        (
            - question: "What are the steps for code injection?"
            - label: Advanced
            - answer: "1. Inject the code to be executed (shellcode) into a writable memory region (stack, data, heap, etc.). 2. Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow. The return address will be the address of the writable memory region that contains the shellcode."
        )
    ]
    <student response>
    """

class V2(PromptTemplate):

    VARIANT = "v2"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a computer science student enrolled in the course "{course_name}".
    You have carefully studied the lecture content provided below.
    To check your understanding, generate a set of clear, relevant questions you might ask your lecturer.
    Each question should be answerable using only the lecture content.
    """

    USER_PROMPT_TEMPLATE = """
    1. Use the lecture content: "{lecture_content}"

    2. Generate {num_questions} {question_word} and answers based only on this content:
        - Write a clear and concise question.
            - Avoid administrative or course-related questions (e.g., about deadlines, problem sets, or what the lecturer said).
            - Avoid vague or contextless questions. Each question should be understandable on its own.
            - When writing questions, avoid vague references like “this topic,” “in the lecture,” or “according to the course.” If you need to refer to the lecture, use its title, e.g., “in the ‘Code Injection Attacks’ lecture.” If you need to refer to the course, use its full name, e.g., “in the ‘Computer Systems Security’ course.”
        - Assign a difficulty level:
            - Basic: direct factual question (e.g., definitions, lists)
            - Intermediate: involves understanding or explaining relationships between ideas
            - Advanced: requires connecting multiple ideas, reasoning through examples, or analyzing concepts
        - Provide a direct answer from the lecture content.

    3. For each question, present your output with the following structure:
        - question: The question text
        - label: Difficulty level (Basic/Intermediate/Advanced)
        - answer: The answer based on the lecture content.


    Here is an example:

    <lecture content>

    Anatomy of a code injection attack
    Goal of code injection. To hijack the execution of the target application/program toward some code injected by the attacker.
    Unlike overwriting the return address of a function with another return address that may result in the termination of the process by returning a segmentation fault, here we inject a malicious code (shellcode) into a writable memory region.
    How can an attacker perform code injection?
    1. Inject the code to be executed (shellcode) into a writable memory region (stack, data, heap, etc.).
    2. Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow. The return address will be the address of the writable memory region that contains the shellcode.
    To inject code, three elements (NOP sled, shellcode, and shellcode address) need to be present, which compose an injection vector.
    So – an injection vector is composed of:
    1. NOP sled (optional): a sequence of do-nothing instructions (NOP). It is used to ease the exploitation, such that the attacker can jump anywhere inside and will eventually reach the shellcode to execute it.
    2. Shellcode: a sequence of machine instructions executed as a result of a code injection attack. Typically, a shellcode executes a shell (eg, execve(“/bin/sh”)). The shellcode is injected by the attacker into a writable and executable memory region. The address of the writable memory region is called the shellcode address.
    3. Shellcode address: The address of the memory region that contains the shellcode.

    </lecture content>

    <student response>
    [
        (
            - question: "Shellcode"
            - label: Basic
            - answer: "Shellcode: a sequence of machine instructions executed as a result of a code injection attack. Typically, a shellcode executes a shell (eg, execve(“/bin/sh”)). The shellcode is injected by the attacker into a writable and executable memory region."
        ),
        (
            - question: "Shellcode address"
            - label: Basic
            - answer: "The address of the memory region that contains the shellcode."
        ),
        (
            - question: "Goal of code injection attack"
            - label: Intermediate
            - answer: "To hijack the execution of the target application/program toward some code injected by the attacker."
        ),
        (
            - question: "Why alter a code pointer in code injection?"
            - label: Intermediate
            - answer: "Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow."
        ),
        (
            - question: "Why is the NOP sled considered optional in a code injection vector?"
            - label: Advanced
            - answer: "NOP sled (optional): a sequence of do-nothing instructions (NOP). It is used to ease the exploitation, such that the attacker can jump anywhere inside and will eventually reach the shellcode to execute it."
        ),
        (
            - question: "What are the steps for code injection?"
            - label: Advanced
            - answer: "1. Inject the code to be executed (shellcode) into a writable memory region (stack, data, heap, etc.). 2. Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow. The return address will be the address of the writable memory region that contains the shellcode."
        )
    ]
    <student response>
    """


class V3(PromptTemplate):

    VARIANT = "v3"

    SYSTEM_PROMPT_TEMPLATE = """
    You are a computer science student enrolled in the course "{course_name}".
    You have carefully studied the lecture content provided below.
    To check your understanding, generate a set of clear, relevant questions you might ask your lecturer.
    Each question should be answerable using only the lecture content.
    """

    USER_PROMPT_TEMPLATE = """
    Lecture title: "{lecture_title}"
    1. Use the lecture content: "{lecture_content}"

    2. Generate {num_questions} questions and answers:
        - Write a clear and specific question.
            - Avoid vague or overly general questions. Each question should focus on specific concepts or terms.
            - Do NOT need to refer to the lecture or to the course.
            - DO NOT use the following expressions: 
                - in the lecture, in the course, or by the lecturer,
                - according to the lecture, according to the course, according to the lecturer.
            - Do NOT ask questions about course logistics, such as deadlines, assignments, or things the lecturer said.
        - Assign a difficulty level:
            - Basic: direct factual question (e.g., definitions, lists).
            - Intermediate: involves understanding or explaining relationships between ideas.
            - Advanced: requires connecting multiple ideas, reasoning through examples, or analyzing concepts.
        - Provide a direct answer from the lecture content.

    3. For each question, present your output with the following structure:
        - question: The question text
        - label: Difficulty level (Basic/Intermediate/Advanced)
        - answer: The answer based on the lecture content.

    Here is an example:

    <lecture content>

    Anatomy of a code injection attack
    Goal of code injection. To hijack the execution of the target application/program toward some code injected by the attacker.
    Unlike overwriting the return address of a function with another return address that may result in the termination of the process by returning a segmentation fault, here we inject a malicious code (shellcode) into a writable memory region.
    How can an attacker perform code injection?
    1. Inject the code to be executed (shellcode) into a writable memory region (stack, data, heap, etc.).
    2. Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow. The return address will be the address of the writable memory region that contains the shellcode.
    To inject code, three elements (NOP sled, shellcode, and shellcode address) need to be present, which compose an injection vector.
    So – an injection vector is composed of:
    1. NOP sled (optional): a sequence of do-nothing instructions (NOP). It is used to ease the exploitation, such that the attacker can jump anywhere inside and will eventually reach the shellcode to execute it.
    2. Shellcode: a sequence of machine instructions executed as a result of a code injection attack. Typically, a shellcode executes a shell (eg, execve(“/bin/sh”)). The shellcode is injected by the attacker into a writable and executable memory region. The address of the writable memory region is called the shellcode address.
    3. Shellcode address: The address of the memory region that contains the shellcode.

    </lecture content>

    <student response>
    [
        (
            - question: "Shellcode"
            - label: Basic
            - answer: "Shellcode: a sequence of machine instructions executed as a result of a code injection attack. Typically, a shellcode executes a shell (eg, execve(“/bin/sh”)). The shellcode is injected by the attacker into a writable and executable memory region."
        ),
        (
            - question: "Shellcode address"
            - label: Basic
            - answer: "The address of the memory region that contains the shellcode."
        ),
        (
            - question: "Goal of code injection attack"
            - label: Intermediate
            - answer: "To hijack the execution of the target application/program toward some code injected by the attacker."
        ),
        (
            - question: "Why alter a code pointer in code injection?"
            - label: Intermediate
            - answer: "Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow."
        ),
        (
            - question: "Why is the NOP sled considered optional in a code injection vector?"
            - label: Advanced
            - answer: "NOP sled (optional): a sequence of do-nothing instructions (NOP). It is used to ease the exploitation, such that the attacker can jump anywhere inside and will eventually reach the shellcode to execute it."
        ),
        (
            - question: "What are the steps for code injection?"
            - label: Advanced
            - answer: "1. Inject the code to be executed (shellcode) into a writable memory region (stack, data, heap, etc.). 2. Alter a code pointer inside the VA (virtual address) of the process (eg, return address) to hijack the execution flow. The return address will be the address of the writable memory region that contains the shellcode."
        )
    ]
    <student response>
    """