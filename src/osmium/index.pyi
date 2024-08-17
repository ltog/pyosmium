# SPDX-License-Identifier: BSD-2-Clause
#
# This file is part of pyosmium. (https://osmcode.org/pyosmium/)
#
# Copyright (C) 2024 Sarah Hoffmann <lonvia@denofr.de> and others.
# For a full list of authors see the git log.
from typing import List

import osmium.osm

class LocationTable:
    def clear(self) -> None: ...
    def get(self, id: int) -> osmium.osm.Location: ...
    def set(self, id: int, loc: osmium.osm.Location) -> None: ...
    def used_memory(self) -> int: ...


class IdSet:
    def __init__(self) -> None: ...
    def set(self, id: int) -> None: ...
    def unset(self, id: int) -> None: ...
    def get(self, id: int) -> bool: ...
    def empty(self) -> bool: ...
    def clear(self) -> None: ...
    def __len__(self) -> int: ...
    def __contains__(self, id: int) -> bool: ...


def create_map(map_type: str) -> LocationTable: ...
def map_types() -> List[str]: ...
