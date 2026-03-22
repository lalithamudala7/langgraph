from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

class State(TypedDict):
    name: str
    user_feedback: str

def step_1(state: State) -> None:
    print("-----Step 1-----")


def human_feedback(state: State) -> None:
    print("-----Human_feedback-----")

def step_3(state: State) -> None:
    print("-----Step 3-----")

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)


#memory = MemorySaver()
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver.from_conn_string("checkpoints.sqlite")

graph = builder.compile(checkpointer=memory, interrupt_before=["human_feedback"])

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "777"}}

    ##Run part1 first and comment part 2 after running part 1 comment part 2 and run part 1 to see the thread execution
    ##part 1 start
    initial_input = {"input": "hello world"}

    for event in graph.stream(initial_input, thread, stream_mode="values"):
        print(event)

    print(graph.get_state(thread).next)
    ##part 1 end
    
    ##part 2 start
    user_input = input("Tell me how you want to update the state: ")

    graph.update_state(thread, {"user_feedback": user_input}, as_node="human_feedback")
    

    print("--State after update--")
    print(graph.get_state(thread))

    print(graph.get_state(thread).next)

    for event in graph.stream(None, thread, stream_mode="values"):
        print(event)
    ##part 2 end