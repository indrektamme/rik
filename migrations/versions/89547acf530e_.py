"""empty message

Revision ID: 89547acf530e
Revises: 
Create Date: 2022-07-01 10:50:25.690091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89547acf530e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('registry_code', sa.Integer(), nullable=True),
    sa.Column('registered', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('registry_code')
    )
    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=True)
    op.create_table('persons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=100), nullable=True),
    sa.Column('lastname', sa.String(length=100), nullable=True),
    sa.Column('personalcode', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('personalcode')
    )
    op.create_index(op.f('ix_persons_firstname'), 'persons', ['firstname'], unique=True)
    op.create_index(op.f('ix_persons_lastname'), 'persons', ['lastname'], unique=True)
    op.create_table('owners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('owner_as_natural_person', sa.Integer(), nullable=True),
    sa.Column('owner_as_legal_person', sa.Integer(), nullable=True),
    sa.Column('establisher', sa.Boolean(), nullable=True),
    sa.Column('capital', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_as_legal_person'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['owner_as_natural_person'], ['persons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('owners')
    op.drop_index(op.f('ix_persons_lastname'), table_name='persons')
    op.drop_index(op.f('ix_persons_firstname'), table_name='persons')
    op.drop_table('persons')
    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_table('companies')
    # ### end Alembic commands ###
