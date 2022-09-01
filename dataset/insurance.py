from datetime import datetime
from faker import Faker
from faker_vehicle import VehicleProvider
from dataclasses import dataclass, field
import random

ID_SIZE = 8
faker = Faker("en-US")
faker.add_provider(VehicleProvider)
Faker.seed(0)
random.seed(0)


def _random_id():
    return faker.uuid4()[:ID_SIZE]


def _random_policy_type():
    return random.choice(["COMPREHENSIVE", "COLLISION", "MEDICAL", "LIABILITY"])


def _random_policy_premium():
    return random.choice(["A", "B", "C", "D", None])


def _random_injury_type():
    return random.choice(["Head", "Arms", "Legs", "Body", "Neck"])


def _random_claim_amount():
    return round(random.uniform(100, 10000), 2)


def _random_phone_number():
    return f"+1 {faker.msisdn()[3:]}"


@dataclass(frozen=True)
class Individual:
    first_name: str
    last_name: str
    dob: datetime
    drivers_licence: bool
    years_experience: int
    phone: str = field(default_factory=_random_phone_number)
    id: str = field(default_factory=_random_id)


@dataclass(frozen=True)
class Address:
    street_name: str
    city: str
    country: str
    id: str = field(default_factory=_random_id)


@dataclass(frozen=True)
class Vehicle:
    type: str
    model: str
    year: int
    price: float
    owner_no: int = field(default_factory=lambda: random.randint(1, 5))
    id: str = field(default_factory=_random_id)


@dataclass(frozen=True)
class Policy:
    start_date: datetime
    end_date: datetime
    type: str = field(default_factory=_random_policy_type)
    premium: str = field(default_factory=_random_policy_premium)
    id: str = field(default_factory=_random_id)


@dataclass(frozen=True)
class Incident:
    accident_date: datetime
    file_date: datetime
    id: str = field(default_factory=_random_id)


@dataclass(frozen=True)
class Claim:
    fraud: bool
    amount: float = field(default_factory=_random_claim_amount)
    id: str = field(default_factory=_random_id)


@dataclass(frozen=True)
class ClaimPayment:
    amount: float
    id: str = field(default_factory=_random_id)


@dataclass(frozen=True)
class Injury:
    type: str = field(default_factory=_random_injury_type)
    id: str = field(default_factory=_random_id)


def random_address():
    return Address(
        street_name=faker.street_address(),
        city=faker.city(),
        country=faker.state(),
    )
