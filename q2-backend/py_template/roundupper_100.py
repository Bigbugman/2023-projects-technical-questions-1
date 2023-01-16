from dataclasses import dataclass
from enum import Enum
import json
import math
from typing import Union, NamedTuple, List
from flask import Flask, Response, request

# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location

# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    # TODO: implement me
    entities: List[SpaceEntity] = request.get_json('entities')
    for entity in entities:
        new = SpaceEntity(entity['metadata'], entity['location'])
        space_database.append(new)

    return json.dumps({})

# lasooable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    # TODO: implement me
    cowboyName = request.args.get('cowboy_name')
    cowboy = None
    for entity in space_database:
        if entity['type'] == "space_cowboy" and entity['metadata']['name'] == cowboyName:
            cowboy = entity
    if len(cowboy) == 0:
        print(f"Failed to find a cowboy with name {cowboyName}")
        return Response(status=400)

    loc_x = cowboy.location['x']
    loc_y = cowboy.location['y']

    entity_list = []

    for entity in space_database:
        x = entity.location['x']
        y = entity.location['y']
        distance = math.sqrt(pow(loc_x-x, 2) + pow(loc_y-y, 2))

        if distance <= cowboy.metadata['lassoLength'] and 'name' not in entity.metadata:
            entity_list.append(
                {
                "type": entity.metadata,
                "location": entity.location
            })

    return json.dumps({"space_animals": entity_list})


# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)
