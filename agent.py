import json
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from tools.tools import calculate_budget, search_flights, search_hotels

load_dotenv()

# read system prompt
current_dir = Path(__file__).parent.resolve()
system_path = current_dir / "prompts" / "system_prompts.xml"
with open(system_path, "r") as f:
    SYSTEM_PROMPT = f.read()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


tools_list = [search_flights, search_hotels, calculate_budget]

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)


# agent node
#
def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # LOGGING
    if response.tool_calls:
        for call in response.tool_calls:
            print(f"Tool call: {call}")
    else:
        print("Direct response")

    return {"messages": [response]}


builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
builder.add_edge("tools", "agent")

graph = builder.compile()


def main():
    print("=" * 60)
    print("TravelBuddy — Trợ lý Du lịch Thông minh")
    print("	Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": [("human", user_input)]})
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")


# {
#   "id": "Test 3",
#   "name": "Multi-Step Tool Chaining",
#   "user_input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
#   "expected_outcome": "Chain: search_flights -> search_hotels -> calculate_budget -> Final summary table",
#   "tool_call": true,
#   "tool_chain": [
#     "search_flights",
#     "search_hotels",
#     "calculate_budget"
#   ]
# },
# call tests from ./tests/tests.json, taking user_input from each test and verifying the output, log the output into
# ./logs/test_logs.txt


def test():
    base_dir = Path(__file__).parent.resolve()
    test_file = base_dir / "tests" / "test.json"
    log_file = base_dir / "logs" / "test_logs.txt"

    log_file.parent.mkdir(parents=True, exist_ok=True)

    if not test_file.exists():
        print(f"Test file not found at {test_file}")
        return

    tests = json.loads(test_file.read_text(encoding="utf-8"))

    with log_file.open("w", encoding="utf-8") as f:
        for test in tests:
            user_input = test["user_input"]
            expected_desc = test["expected_outcome"]
            test_id = test.get("id", "Unknown")

            # Run the graph
            result = graph.invoke({"messages": [("human", user_input)]})

            # 1. Extract all tool calls made during the process
            actual_tools = []
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for call in msg.tool_calls:
                        actual_tools.append(call["name"])

            # 2. Get the final text response
            # Filter for AIMessages that actually have text content
            text_responses = [
                m.content
                for m in result["messages"]
                if isinstance(m, AIMessage) and m.content
            ]
            final_content = text_responses[-1] if text_responses else "No text response"

            # 3. Logic for Pass/Fail
            # Since we can't do string == string, we check tool usage
            # and log the content for manual review
            tool_call_expected = test.get("tool_call", False)
            tool_match = (len(actual_tools) > 0) == tool_call_expected

            status = (
                "PASS"
                if tool_match
                else f"FAIL: Expected {'at least one tool call' if tool_call_expected else 'a direct response'}, but got {f'calls to {actual_tools}' if actual_tools else 'no tool calls'}"
            )

            output = (
                f"--- Test {test_id}: {test['name']} ---\n"
                f"Input: {user_input}\n"
                f"Expected Goal: {expected_desc}\n"
                f"Actual Tools Called: {actual_tools}\n"
                f"Final Content: {final_content[:300]}...\n"
                f"Status: {status}\n" + "-" * 30 + "\n"
            )

            f.write(output)
            print(f"Ran {test_id}: {status}")


if __name__ == "__main__":
    test()
