from typing import Any, Dict

from autogen_core.tools._base import ParametersSchema, ToolSchema
from playwright.async_api import Page
import os

os.environ["username"]="manideepsitaram143@gmail.com"
os.environ["password"]="kannasitaram"
def _load_tool(tooldef: Dict[str, Any]) -> ToolSchema:
    return ToolSchema(
        name=tooldef["function"]["name"],
        description=tooldef["function"]["description"],
        parameters=ParametersSchema(
            type="object",
            properties=tooldef["function"]["parameters"]["properties"],
            required=tooldef["function"]["parameters"]["required"],
        ),
    )


REASONING_TOOL_PROMPT = (
    "A short description of the action to be performed and reason for doing so, do not mention the user."
)

TOOL_VISIT_URL: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "visit_url",
            "description": "Navigate directly to a provided URL using the browser's address bar. Prefer this tool over other navigation techniques in cases where the user provides a fully-qualified URL (e.g., choose it over clicking links, or inputing queries into search boxes).",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                    "url": {
                        "type": "string",
                        "description": "The URL to visit in the browser.",
                    },
                },
                "required": ["reasoning", "url"],
            },
        },
    }
)

TOOL_WEB_SEARCH: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Performs a web search on Bing.com with the given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                    "query": {
                        "type": "string",
                        "description": "The web search query to use.",
                    },
                },
                "required": ["reasoning", "query"],
            },
        },
    }
)

TOOL_HISTORY_BACK: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "history_back",
            "description": "Navigates back one page in the browser's history. This is equivalent to clicking the browser back button.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                },
                "required": ["reasoning"],
            },
        },
    }
)

TOOL_SCROLL_UP: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "scroll_up",
            "description": "Scrolls the entire browser viewport one page UP towards the beginning.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                },
                "required": ["reasoning"],
            },
        },
    }
)

TOOL_SCROLL_DOWN: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "scroll_down",
            "description": "Scrolls the entire browser viewport one page DOWN towards the end.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                },
                "required": ["reasoning"],
            },
        },
    }
)

TOOL_CLICK: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "click",
            "description": "Clicks the mouse on the target with the given id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                    "target_id": {
                        "type": "integer",
                        "description": "The numeric id of the target to click.",
                    },
                },
                "required": ["reasoning", "target_id"],
            },
        },
    }
)

TOOL_TYPE: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "input_text",
            "description": "Types the given text value into the specified field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                    "input_field_id": {
                        "type": "integer",
                        "description": "The numeric id of the input field to receive the text.",
                    },
                    "text_value": {
                        "type": "string",
                        "description": "The text to type into the input field.",
                    },
                },
                "required": ["reasoning", "input_field_id", "text_value"],
            },
        },
    }
)

TOOL_SCROLL_ELEMENT_DOWN: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "scroll_element_down",
            "description": "Scrolls a given html element (e.g., a div or a menu) DOWN.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                    "target_id": {
                        "type": "integer",
                        "description": "The numeric id of the target to scroll down.",
                    },
                },
                "required": ["reasoning", "target_id"],
            },
        },
    }
)

TOOL_SCROLL_ELEMENT_UP: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "scroll_element_up",
            "description": "Scrolls a given html element (e.g., a div or a menu) UP.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                    "target_id": {
                        "type": "integer",
                        "description": "The numeric id of the target to scroll UP.",
                    },
                },
                "required": ["reasoning", "target_id"],
            },
        },
    }
)

TOOL_HOVER: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "hover",
            "description": "Hovers the mouse over the target with the given id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                    "target_id": {
                        "type": "integer",
                        "description": "The numeric id of the target to hover over.",
                    },
                },
                "required": ["reasoning", "target_id"],
            },
        },
    }
)


TOOL_READ_PAGE_AND_ANSWER: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "answer_question",
            "description": "Uses AI to answer a question about the current webpage's content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                    "question": {
                        "type": "string",
                        "description": "The question to answer.",
                    },
                },
                "required": ["reasoning", "question"],
            },
        },
    }
)

TOOL_SUMMARIZE_PAGE: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "summarize_page",
            "description": "Uses AI to summarize the entire page.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                },
                "required": ["reasoning"],
            },
        },
    }
)

TOOL_SLEEP: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "sleep",
            "description": "Wait a short period of time. Call this function if the page has not yet fully loaded, or if it is determined that a small delay would increase the task's chances of success, or if it is a login page or some authentication page which needs human inputs",
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": REASONING_TOOL_PROMPT,
                    },
                },
                "required": ["reasoning"],
            },
        },
    }
)


async def auto_form_login(page:Page) -> dict:
 # 1. Grab all potential login inputs
    locator = page.locator(
        'input[type="text"], input[type="email"], input[type="password"]'
    )
    inputs = await locator.all()

    # 2. Normalize attribute → ENV key and fill
    for inp in inputs:
        raw = (
            await inp.get_attribute("id")
            or await inp.get_attribute("name")
            or await inp.get_attribute("placeholder")
            or ""
        )
        print(f"This is the raw for {inp} and the raw is {raw}")
        key = raw.strip().upper().replace("-", "_").replace(" ", "_")
        if key in os.environ:
            await inp.fill(os.environ[key])
            print(f"Filled `{raw}` from ENV[{key}]")

    # 3. Submit the form
    await page.click('button[type="submit"], input[type="submit"]')
    print("Form submitted; resuming agent flow.")

    return {"status": "resumed"}


TOOL_AUTOMATIC_LOGIN: ToolSchema = _load_tool(
    {
        "type": "function",
        "function": {
            "name": "automatic_login",
            "description": (
                "Automatically detects all text/email/password fields on the login page, "
                "fills them from matching environment variables, submits the form, "
                "and returns a status dict."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "page": {
                        "type": "object",
                        "description": "A Playwright Page instance representing the current browser page."
                    }
                },
                "required": ["page"]
            }
        }
    }
)
