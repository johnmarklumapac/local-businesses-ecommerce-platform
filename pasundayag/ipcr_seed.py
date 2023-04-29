from django_seed import Seed
from .models import IPCR

def seed_IPCR():
    seeder = Seed.seeder()
    seeder.add_entity(IPCR, 10)
    inserted_pks = seeder.execute()
    print(inserted_pks)