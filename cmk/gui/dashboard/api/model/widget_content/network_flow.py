#!/usr/bin/env python3
# Copyright (C) 2026 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
from typing import Literal, override, Self

from cmk.gui.dashboard.type_defs import (
    NetworkFlowBarAccent,
    NetworkFlowTopTableDashletConfig,
    NetworkFlowTopTableDimension,
)
from cmk.gui.openapi.framework.model import api_field, api_model

from ._base import BaseWidgetContent


@api_model
class NetworkFlowTopTableContent(BaseWidgetContent):
    type: Literal["network_flow_top_table"] = api_field(
        description="Displays top-N network flow entities ranked by volume with inline bars."
    )
    dimension: NetworkFlowTopTableDimension = api_field(
        description="Which entity dimension to rank (local hosts, remote hosts, applications "
        "or autonomous systems)."
    )
    accent: NetworkFlowBarAccent = api_field(description="Accent color of the inline bars.")
    limit_to: int = api_field(description="Maximum number of rows to display.")

    @classmethod
    @override
    def internal_type(cls) -> str:
        return "network_flow_top_table"

    @classmethod
    def from_internal(cls, config: NetworkFlowTopTableDashletConfig) -> Self:
        return cls(
            type="network_flow_top_table",
            dimension=config["dimension"],
            accent=config["accent"],
            limit_to=config["limit_to"],
        )

    @override
    def to_internal(self) -> NetworkFlowTopTableDashletConfig:
        return NetworkFlowTopTableDashletConfig(
            type=self.internal_type(),
            dimension=self.dimension,
            accent=self.accent,
            limit_to=self.limit_to,
        )
