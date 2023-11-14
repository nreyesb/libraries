# -*- coding: utf-8 -*-
"""
Private License - For Internal Use Only

Copyright (c) 2023 Toku
All rights reserved.

This software is provided for internal use only and may not be
distributed, reproduced, or disclosed to any third party without
prior written permission from Toku.

Module: main.py
Author: Toku
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from toku.storage.url.core import StorageUrlException
from toku.storage.url.verifier.api import StorageUrlVerificationException
from toku.storage.url.api.verifier import UnauthorizedStorageUrlVerificationException
from toku.storage.url.api.verifier import ForbiddenStorageUrlVerificationException
from toku.storage.url.api.verifier import ConflictStorageUrlVerificationException
from src.application.routers import url_router

app = FastAPI()


# middleware
@app.exception_handler(UnauthorizedStorageUrlVerificationException)
async def unauthorized_storage_url_verification_exception_handler(
    _request: Request,
    exception: StarletteHTTPException
) -> JSONResponse:
    """
    Return a JSONResponse with HTTP status code 401.
    """
    return JSONResponse(
        content={"detail": str(exception)},
        status_code=401
    )


@app.exception_handler(ForbiddenStorageUrlVerificationException)
async def forbidden_storage_url_verification_exception_handler(
    _request: Request,
    exception: StarletteHTTPException
) -> JSONResponse:
    """
    Return a JSONResponse with HTTP status code 403.
    """
    return JSONResponse(
        content={"detail": str(exception)},
        status_code=403
    )


@app.exception_handler(ConflictStorageUrlVerificationException)
async def conflict_storage_url_verification_exception_handler(
    _request: Request,
    exception: StarletteHTTPException
) -> JSONResponse:
    """
    Return a JSONResponse with HTTP status code 409.
    """
    return JSONResponse(
        content={"detail": str(exception)},
        status_code=409
    )


@app.exception_handler(StorageUrlVerificationException)
async def storage_url_verification_exception_handler(
    _request: Request,
    exception: StarletteHTTPException
) -> JSONResponse:
    """
    Return a JSONResponse with HTTP status code 500.
    """
    return JSONResponse(
        content={"detail": str(exception)},
        status_code=500
    )


@app.exception_handler(StorageUrlException)
async def storage_url_exception_handler(
    _request: Request,
    exception: StarletteHTTPException
) -> JSONResponse:
    """
    Return a JSONResponse with HTTP status code 500.
    """
    return JSONResponse(
        content={"detail": str(exception)},
        status_code=500
    )


@app.exception_handler(Exception)
async def exception_handler(
    _request: Request,
    _exception: StarletteHTTPException
) -> JSONResponse:
    """
    Return a JSONResponse with HTTP status code `exception.status_code`
    to avoid raise a Sentry error.
    """
    return JSONResponse(
        content={"detail": "Internal Error"},
        status_code=500
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    _request: Request,
    exception: StarletteHTTPException
) -> JSONResponse:
    """
    Return a JSONResponse with HTTP status code `exception.status_code`
    to avoid raise a Sentry error.
    """
    return JSONResponse(
        content={"detail": exception.detail},
        status_code=exception.status_code
    )

# routers
app.include_router(url_router.router)
