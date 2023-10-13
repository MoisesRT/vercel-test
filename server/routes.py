import os
import re

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

router = APIRouter()

from redis import Redis


def get_redis_kwargs():
    # KV_URL="redis://default:e5626a2f3fef4341835344118945ca7c@concrete-parrot-33991.kv.vercel-storage.com:33991"
    kv_url = os.environ.get('KV_URL')
    if not kv_url:
        return {}
    username, password, host, port = re.search(
        r'redis://(.*):(.*)@(.*):(.*)', kv_url).groups()
    return {
        'host': host,
        'port': port,
        'username': username,
        'password': password
    }


kv = Redis(**get_redis_kwargs())


def get_notes_from_kv():
    return kv.get('notes')


@router.get("/")
async def get_notes() -> dict:
    return get_notes_from_kv()


@router.get("/{id}")
async def get_note(id: str) -> dict:
    return get_notes_from_kv().get(id)


@router.post("/")
async def add_note(note: dict = Body(...)) -> dict:
    notes = get_notes_from_kv()
    notes.update({note['id']: jsonable_encoder(note)})
    await kv.set('notes', notes)
    return notes
