from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Models.organizations.organizationsModel import Organizations
from Schemas.organizationSchema.organization_Shema import OrganizationCreate, OrganizationUpdate


# -------------------------
# GET ALL
# -------------------------
async def get_organizations(db: AsyncSession):
    result = await db.execute(select(Organizations))
    return result.scalars().all()


# -------------------------
# GET BY ID
# -------------------------
async def get_organization(db: AsyncSession, org_id: int):
    return await db.get(Organizations, org_id)


# -------------------------
# CREATE
# -------------------------
async def create_organization(db: AsyncSession, data: OrganizationCreate):
    org = Organizations(**data.dict())
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org


# -------------------------
# UPDATE
# -------------------------
async def update_organization(
    db: AsyncSession,
    org_id: int,
    data: OrganizationUpdate
):
    org = await db.get(Organizations, org_id)
    if not org:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(org, key, value)

    await db.commit()
    await db.refresh(org)
    return org


# -------------------------
# DELETE
# -------------------------
async def delete_organization(db: AsyncSession, org_id: int):
    org = await db.get(Organizations, org_id)
    if not org:
        return None

    await db.delete(org)
    await db.commit()
    return org
