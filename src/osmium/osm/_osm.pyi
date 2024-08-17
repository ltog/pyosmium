# SPDX-License-Identifier: BSD-2-Clause
#
# This file is part of pyosmium. (https://osmcode.org/pyosmium/)
#
# Copyright (C) 2024 Sarah Hoffmann <lonvia@denofr.de> and others.
# For a full list of authors see the git log.
from typing import ClassVar, Iterator, Tuple, Optional, Any

from typing import overload
import datetime

import osmium.osm.mutable

ALL: osm_entity_bits
AREA: osm_entity_bits
CHANGESET: osm_entity_bits
NODE: osm_entity_bits
NOTHING: osm_entity_bits
OBJECT: osm_entity_bits
RELATION: osm_entity_bits
WAY: osm_entity_bits


class Location:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, lon: float, lat: float) -> None: ...
    def lat_without_check(self) -> float: ...
    def lon_without_check(self) -> float: ...
    def valid(self) -> bool: ...
    @property
    def lat(self) -> float: ...
    @property
    def lon(self) -> float: ...
    @property
    def x(self) -> int: ...
    @property
    def y(self) -> int: ...

class Box:
    @overload
    def __init__(self, minx: float, miny: float, maxx: float, maxy: float) -> None: ...
    @overload
    def __init__(self, bottom_left: Location, top_right: Location) -> None: ...
    def contains(self, location: Location) -> bool: ...
    @overload
    def extend(self, location: Location) -> Box: ...
    @overload
    def extend(self, box: Box) -> Box: ...
    def size(self) -> float: ...
    def valid(self) -> bool: ...
    @property
    def bottom_left(self) -> Location: ...
    @property
    def top_right(self) -> Location: ...

class CTagListIterator:
    pass

class CRelationMemberListIterator:
    pass

class BufferProxyProtocol:
    def is_valid(self) -> bool: ...

class NodeRefList:
    def ends_have_same_location(self, parent: BufferProxyProtocol) -> bool: ...
    def is_closed(self, parent: BufferProxyProtocol) -> bool: ...
    def get(self, parent: BufferProxyProtocol, idx: int) -> osmium.osm.types.NodeRef: ...
    def size(self, parent: BufferProxyProtocol) -> int: ...

class CWayNodeList(NodeRefList):
    pass

class COuterRing(NodeRefList):
    pass

class CInnerRing(NodeRefList):
    pass

class COuterRingIterator:
    pass

class CInnerRingIterator:
    pass

class TagContainerProtocol(BufferProxyProtocol):
    def tags_size(self) -> int: ...
    def tags_get_value_by_key(self, key: str, default: Optional[str]) -> Optional[str]: ...
    def tags_has_key(self, key: str) -> bool: ...
    def tags_begin(self) -> CTagListIterator: ...
    def tags_next(self, it: CTagListIterator) -> osmium.osm.types.Tag: ...

class COSMObject(TagContainerProtocol):
    def positive_id(self) -> int: ...
    def user_is_anonymous(self) -> bool: ...
    def changeset(self) -> int: ...
    def deleted(self) -> bool: ...
    def id(self) -> int: ...
    def timestamp(self) -> datetime.datetime: ...
    def uid(self) -> int: ...
    def user(self) -> str: ...
    def version(self) -> int: ...
    def visible(self) -> bool: ...

class COSMNode(COSMObject):
    def location(self) -> Location: ...

class COSMWay(COSMObject):
    def ends_have_same_id(self) -> bool: ...
    def ends_have_same_location(self) -> bool: ...
    def is_closed(self) -> bool: ...
    def nodes(self) -> CWayNodeList: ...

class COSMRelation(COSMObject):
    def members_size(self) -> int: ...
    def members_begin(self) -> CRelationMemberListIterator: ...
    def members_next(self, it: CRelationMemberListIterator) -> osmium.osm.types.RelationMember: ...

class COSMArea(COSMObject):
    def from_way(self) -> bool: ...
    def inner_rings(self, outer_ring: COuterRing) -> CInnerRingIterator: ...
    def is_multipolygon(self) -> bool: ...
    def num_rings(self) -> Tuple[int,int]: ...
    def orig_id(self) -> int: ...
    def outer_begin(self) -> COuterRingIterator: ...
    def outer_next(self, it: COuterRingIterator) -> COuterRing: ...
    def inner_begin(self, oring: COuterRing) -> CInnerRingIterator: ...
    def inner_next(self, it: CInnerRingIterator) -> CInnerRing: ...

class COSMChangeset(TagContainerProtocol):
    def user_is_anonymous(self) -> bool: ...
    def bounds(self) -> Box: ...
    def closed_at(self) -> datetime.datetime: ...
    def created_at(self) -> datetime.datetime: ...
    def id(self) -> int: ...
    def num_changes(self) -> int: ...
    def open(self) -> bool: ...
    def uid(self) -> int: ...
    def user(self) -> str: ...

class osm_entity_bits:
    ALL: ClassVar[osm_entity_bits] = ...
    AREA: ClassVar[osm_entity_bits] = ...
    CHANGESET: ClassVar[osm_entity_bits] = ...
    NODE: ClassVar[osm_entity_bits] = ...
    NOTHING: ClassVar[osm_entity_bits] = ...
    OBJECT: ClassVar[osm_entity_bits] = ...
    RELATION: ClassVar[osm_entity_bits] = ...
    WAY: ClassVar[osm_entity_bits] = ...
    def __init__(self, value: int) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...
    def __or__(self, other: osm_entity_bits) -> osm_entity_bits: ...
    def __and__(self, other: osm_entity_bits) -> osm_entity_bits: ...
    def __invert__(self) -> osm_entity_bits: ...
    def __bool__(self) -> bool: ...
