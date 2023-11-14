# -*- coding: utf-8 -*-
# pylint: disable=useless-import-alias
# pylint: disable=line-too-long
"""
This package provides the source code to support the project.

Packages:
    - application: Provides the application layer to expose the logic to the world.
                   It interacts with the domain layer.
    - common: Provides common processes for each layers.
    - domain: Provides the domain layer to expose the bussines logic.
              It is used by the application layer and interacts with the infrastructure layer.
    - infrastructure: Provides the infrastructure layer to expose the respository / recipient logic.
                      It is used by the domain layer.
"""
