#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.gui.graphing.openapi._family import GRAPH_FAMILY
from cmk.gui.graphing.openapi.models import AddToRequest
from cmk.gui.openapi.framework import (
    APIVersion,
    EndpointDoc,
    EndpointHandler,
    EndpointMetadata,
    EndpointPermissions,
    VersionedEndpoint,
)
from cmk.gui.openapi.restful_objects.constructors import domain_type_action_href


def add_to_visual_v1(body: AddToRequest) -> None:
    """Add a graph to a visual container"""
    # TODO: To be implemented in CMK-36344
    # TODO: Adjust the return type to a proper response model once the implementation is done


ENDPOINT_ADD_TO_VISUAL = VersionedEndpoint(
    metadata=EndpointMetadata(
        path=domain_type_action_href("graph", "add_to_visual"),
        link_relation=".../action-param",
        method="post",
        content_type=None,  # Remove if the endpoint returns data
    ),
    permissions=EndpointPermissions(),
    doc=EndpointDoc(family=GRAPH_FAMILY.name),
    versions={APIVersion.INTERNAL: EndpointHandler(handler=add_to_visual_v1)},
)
