WEB_SURFER_TOOL_PROMPT_MM = """ 
Important: If the Current Page is Login Page then use automatic_login tool
{state_description}

Consider the following screenshot of the page. In this screenshot, interactive elements are outlined in bounding boxes of different colors. Each bounding box has a numeric ID label in the same color. Additional information about each visible label is listed below:

{visible_targets}{other_targets_str}{focused_hint}

You are to respond to my request by selecting an appropriate tool from the following set, or by answering the question directly if possible:

{tool_names}

When deciding between tools, consider if the request can be best addressed by:
    - the contents of the CURRENT VIEWPORT (in which case actions like clicking links, clicking buttons, inputting text, or hovering over an element might be more appropriate)
    - contents found elsewhere on the CURRENT WEBPAGE [{title}]({url}), in which case actions like scrolling, summarization, or full-page Q&A might be most appropriate
    - on ANOTHER WEBSITE entirely (in which case actions like performing a new web search might be the best option)
    - for anything related to authentication on the Login Page, actions related to authentication (e.g., entering credentials, submitting login forms) automatic_login tool should be prioritized

**Important**: You must strictly adhere to the following user request and keep its goal in mind at all times:  
**User Request**: {user_request}  
Only execute actions or provide responses that are directly aligned with this request. Do not deviate from the specified goal under any circumstances.

My request follows:
"""

WEB_SURFER_TOOL_PROMPT_TEXT = """
{state_description}

You have also identified the following interactive components:

{visible_targets}{other_targets_str}{focused_hint}

You are to respond to my next request by selecting an appropriate tool from the following set, or by answering the question directly if possible:

{tool_names}

When deciding between tools, consider if the request can be best addressed by:
    - the contents of the CURRENT VIEWPORT (in which case actions like clicking links, clicking buttons, inputting text, or hovering over an element, might be more appropriate)
    - contents found elsewhere on the CURRENT WEBPAGE [{title}]({url}), in which case actions like scrolling, summarization, or full-page Q&A might be most appropriate
    - on ANOTHER WEBSITE entirely (in which case actions like performing a new web search might be the best option)

My request follows:
"""


WEB_SURFER_QA_SYSTEM_MESSAGE = """
You are a helpful assistant that can summarize long documents to answer question.
"""


def WEB_SURFER_QA_PROMPT(title: str, question: str | None = None) -> str:
    base_prompt = f"We are visiting the webpage '{title}'. Its full-text content are pasted below, along with a screenshot of the page's current viewport."
    if question is not None:
        return (
            f"{base_prompt} Please summarize the webpage into one or two paragraphs with respect to '{question}':\n\n"
        )
    else:
        return f"{base_prompt} Please summarize the webpage into one or two paragraphs:\n\n"
