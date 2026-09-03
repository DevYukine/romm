"""Add ROM-internal title ids extracted by rom-converto

Revision ID: 0116_add_title_ids
Revises: 0115_add_steam_metadata
Create Date: 2026-09-02 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op  # type: ignore[attr-defined]

# revision identifiers, used by Alembic.
revision = "0116_add_title_ids"
down_revision = "0115_add_steam_metadata"
branch_labels = None
depends_on = None

# BigInteger because Switch title versions exceed int32.
_NEW_COLUMNS: list[tuple[str, sa.types.TypeEngine]] = [
    ("roms", "title_id", sa.String(length=100)),
    ("rom_files", "title_id", sa.String(length=100)),
    ("rom_files", "title_version", sa.BigInteger()),
]


def upgrade() -> None:
    for table, name, column_type in _NEW_COLUMNS:
        op.add_column(table, sa.Column(name, column_type, nullable=True))

    op.create_index("idx_roms_title_id", "roms", ["title_id"], unique=False)
    op.create_index(
        "idx_rom_files_title_id", "rom_files", ["title_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("idx_rom_files_title_id", table_name="rom_files")
    op.drop_index("idx_roms_title_id", table_name="roms")

    for table, name, _ in reversed(_NEW_COLUMNS):
        op.drop_column(table, name)
