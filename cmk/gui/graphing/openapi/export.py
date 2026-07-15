#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.gui.graphing.openapi._family import GRAPH_FAMILY
from cmk.gui.graphing.openapi.models import ExportRequest
from cmk.gui.openapi.framework import (
    APIVersion,
    EndpointDoc,
    EndpointHandler,
    EndpointMetadata,
    EndpointPermissions,
    VersionedEndpoint,
)
from cmk.gui.openapi.restful_objects.constructors import domain_type_action_href


def export_v1(body: ExportRequest) -> None:
    """Export a graph"""
    # TODO: To be implemented in CMK-36344
    # TODO: Adjust the return type to a proper response model once the implementation is done


ENDPOINT_EXPORT = VersionedEndpoint(
    metadata=EndpointMetadata(
        path=domain_type_action_href("graph", "export"),
        link_relation="cmk/download",
        method="post",
        content_type=None,  # Remove if the endpoint returns data
    ),
    permissions=EndpointPermissions(),
    doc=EndpointDoc(family=GRAPH_FAMILY.name),
    versions={APIVersion.INTERNAL: EndpointHandler(handler=export_v1)},
)
