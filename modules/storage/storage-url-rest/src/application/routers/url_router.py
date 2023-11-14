# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: url_router.py
Author: Toku
"""
from typing import AsyncGenerator
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, StreamingResponse
from toku.storage.url.core import UrlStreaming
from toku.storage.url.api import StorageUrl
from src.application.models import UrlModel
from src.application.models import UrlMetadataModel
from src.application.mappers import UrlModelMapper
from src.application.mappers import UrlMetadataModelMapper
from src.domain.services import UrlEncodeService
from src.domain.services import UrlDecodeService
from src.domain.services import UrlStreamingService
from src.infrastructure.factories.storage_driver_factory import StorageDriverFactory
from src.infrastructure.repository.storage import UrlEncodeRepository
from src.infrastructure.repository.storage import UrlDecodeRepository
from src.infrastructure.repository.storage import UrlStreamingRepository
from src.infrastructure.factories import StorageUrlFactory


STORAGE_URL_BUILTIN = "BUILT-IN"

router = APIRouter(
    prefix="/api/v1/storage/url",
    # tags=["items"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.post("/encode")
async def encode(url: UrlModel, url_metadata: UrlMetadataModel) -> PlainTextResponse:
    url_encode_service: UrlEncodeService = UrlEncodeService(
        UrlEncodeRepository(
            StorageUrlFactory().create(STORAGE_URL_BUILTIN)
        )
    )

    return PlainTextResponse(
        url_encode_service.encode(
            url=UrlModelMapper().map(url),
            url_metadata=UrlMetadataModelMapper().map(url_metadata)
        )
    )


@router.get("/decode/{metadata}")
async def decode(metadata: str) -> UrlMetadataModel:
    url_decode_service: UrlDecodeService = UrlDecodeService(
        UrlDecodeRepository(
            StorageUrlFactory().create(STORAGE_URL_BUILTIN)
        )
    )

    return UrlMetadataModelMapper().unmap(url_decode_service.decode(metadata))


@router.get("/streaming/{metadata}")
async def streaming(metadata: str) -> StreamingResponse:
    storage_url: StorageUrl = StorageUrlFactory().create(STORAGE_URL_BUILTIN)
    url_streaming_service: UrlStreamingService = UrlStreamingService(
        UrlDecodeRepository(
            storage_url
        ),
        UrlStreamingRepository(
            storage_driver_factory=StorageDriverFactory(),
            storage_url=storage_url
        )
    )
    url_streaming: UrlStreaming = url_streaming_service.streaming(metadata)

    # generator function to yield chunks of data from the BufferedReader
    async def generate() -> AsyncGenerator[bytes, None]:
        with url_streaming as input_stream:
            while True:
                chunk = input_stream.data.read(1024)  # read data in 1 KB chunks
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(
        content=generate(),
        media_type=url_streaming.content_type,
        headers={
            'Content-Disposition': 'attachment; filename="' + url_streaming.name + '"'
        }
    )
