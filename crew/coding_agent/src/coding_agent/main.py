#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from coding_agent.crew import CodingAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():

    assignment = 'Write a python program to calculate  the angle at which a missile launcher must be aimed based on distance, wind speed and speed of the missile'

    inputs ={
        'assignment': assignment
    }

    try:
        CodingAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


