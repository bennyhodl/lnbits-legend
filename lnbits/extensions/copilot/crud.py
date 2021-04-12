from typing import List, Optional, Union

# from lnbits.db import open_ext_db
from . import db
from .models import Copilots

from lnbits.helpers import urlsafe_short_hash

from quart import jsonify


###############COPILOTS##########################


async def create_copilot(
    title: str,
    user: str,
    animation: str = None,
    show_message: Optional[str] = None,
    amount: Optional[str] = None,
    lnurl_title: Optional[str] = None,
) -> Copilots:
    copilot_id = urlsafe_short_hash()

    await db.execute(
        """
        INSERT INTO copilots (
            id,
            user,
            title,
            animation,
            show_message,
            amount,
            lnurl_title
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            copilot_id,
            user,
            title,
            animation,
            show_message,
            amount,
            lnurl_title
        ),
    )
    return await get_copilot(copilot_id)


async def update_copilot(copilot_id: str, **kwargs) -> Optional[Copilots]:
    q = ", ".join([f"{field[0]} = ?" for field in kwargs.items()])
    await db.execute(
        f"UPDATE copilots SET {q} WHERE id = ?", (*kwargs.values(), copilot_id)
    )
    row = await db.fetchone("SELECT * FROM copilots WHERE id = ?", (copilot_id,))
    return Copilots.from_row(row) if row else None


async def get_copilot(copilot_id: str) -> Copilots:
    row = await db.fetchone("SELECT * FROM copilots WHERE id = ?", (copilot_id,))
    return Copilots.from_row(row) if row else None


async def get_copilots(user: str) -> List[Copilots]:
    rows = await db.fetchall("SELECT * FROM copilots WHERE user = ?", (user,))
    return [Copilots.from_row(row) for row in rows]


async def delete_copilot(copilot_id: str) -> None:
    await db.execute("DELETE FROM copilots WHERE id = ?", (copilot_id,))
