import os
import openai
from logger import Logger

def generate_prompt(checklist, item_idx):
        prompt = f'You are the assistant to a patent attorney. Your are given a checklist item, and your job is to determine whether the section on "power processing system" adheres to the given checklist item or not. If it does, point to the place in the paragraph where it does. If it does not, brainstorm ideas on how to add to the paragraph to make it so. \n ### CHECKLIST ITEM: {checklist[item_idx]}'

        return prompt

def test_review(model, model_name: str):
    logger = Logger()
    logger.init_experiment()
    checklist = [
    """**Introduces of Element(s) or Step(s)**
    - Clearly introduce the main element or step being described.
    - E.g., 'Receiving a measurement set S100', 'The emitter array 100'""",
    """**Talks about the Primary Function**
    - Describe the primary function or purpose of the introduced element/step.
    - E.g., "functions to obtain information", 'functions to emit (e.g., eject, release, disperse, etc.) working material.'""",
    """**Talks about the preferred configuration/variant**
    - Indicate a preferred configuration or variant of the element or step.
    - E.g., 'The measurement set preferably includes', 'The emitter array preferably includes'""",
    """**Talks about alternative configurations**
    - Mention alternatives or other configurations/variations of the element or step.
    - E.g., 'but can alternatively include', 'but can include a single emitter'""",
    """**Talks about specifics, details or examples**
    - Dive into specifics, finer details, or illustrative examples of the element or step.
    - E.g., 'e.g., an image, a video', 'via a manifold, propellant management device, etc.'""",
    """**Talks about optional features or steps**
    - Discuss optional features, steps, or characteristics that can be added or considered.
    - E.g., 'S100 can optionally include determining metadata', 'The emitter array is preferably in fluid communication with a reservoir 180'""",
    """**Talks about additional components or sub-elements**
    - If applicable, talk about related components or sub-elements that interact with or relate to the main element/step.
    - E.g., 'The metadata is preferably determined by and received from the source sensor system', 'The emitter array is preferably aligned to an electrode'""",
    """**Talks about specific values or ranges**
    - If applicable, provide specific values, measurements, or ranges associated with the element/step.
    - E.g., 'spacing between the tip of the emitter array is preferably between about 0 and 1000 µm', 'e.g., 0—50 µm, 10—50µm, 20—60 µm'""",
    """**Talks about elaborate variants or special cases**
    - Mention any special cases, elaborative variants, or exceptions.
    - E.g., 'In the latter variant, the method can optionally crop, resize, infill', 'In some variants (e.g., for a curved emitter array such as emitters on a curved substrate; for a curved electrode such as an electrode with a concave, convex, serpentine, etc. surface; for emitter arrays that include emitters with varying heights, etc.)'""",
    """**Talks about the broad application or general notes**
    - Indicate the broader scope or general remarks to allow flexibility in interpretation.
    - E.g., 'and/or any other suitable measurement', 'and/or other working fluid source', 'and/or the emitter array and electrode(s) can have any suitable separation.'"""
    ]

    prompts = []
    responses = []
    for i in range(len(checklist)):
        prompt = generate_prompt(checklist, i)
        prompts.append(prompt)
        responses.append(model.query(prompt))

    r_str = ''
    for response in responses:
        r_str += str(response) + '\n'
        
    logger.save_to_file(r_str, file_name=f'{model_name}.txt')
