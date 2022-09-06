"""
Generate parquet files with table data for insurance claims.
Usage:
    python data_generator <TOTAL_FAMILIES> <TOTAL_INCIDENTS>

Example of parameters: 1000 300
"""

from dateutil.relativedelta import relativedelta
from insurance import (
    Claim,
    ClaimPayment,
    Incident,
    Individual,
    Injury,
    Policy,
    Vehicle,
)
from insurance import random, faker, datetime, random_address
import numpy as np
import pandas as pd
import sys
import os

from table_generator import (
    address_data,
    claim_data,
    incident_data,
    incident_individual_data,
    individual_data,
    injury_data,
    payment_data,
    policy_data,
    store_address,
    store_claim,
    store_claim_payment,
    store_incident,
    store_individual,
    store_injury,
    store_policy,
    store_vehicle,
    vehicle_data,
)


def generate_family():
    individuals = []
    members = random.randint(1, 4)

    last_name = faker.last_name()
    for _ in range(members):
        licence = bool(random.randint(0, 1))
        experience = random.randint(1, 20) if licence else 0
        individual = Individual(
            first_name=faker.first_name(),
            last_name=last_name,
            dob=faker.date_of_birth(None, 18, 80),
            drivers_licence=licence,
            years_experience=experience,
        )
        individuals.append(individual)

    address = random_address()
    return (individuals, address)


def generate_policy(individual: Individual):
    policies = []
    vehicles = []

    if not individual.drivers_licence:
        return policies, vehicles
    # The largest probability is either 1 or 0
    for _ in range(int(np.random.poisson(1, 1))):
        start_date = faker.date_between_dates(
            date_start=datetime.now() - relativedelta(years=2), date_end=datetime.now()
        )
        end_date = faker.date_between_dates(
            date_start=start_date, date_end=datetime.now() + relativedelta(years=2)
        )
        policy = Policy(start_date=start_date, end_date=end_date)

        if random.random() > 0.9:
            vehicle_type = "Machine"
            vehicle_object = faker.machine_object()
        else:
            vehicle_type = "Vehicle"
            vehicle_object = faker.vehicle_object()

        vehicle = Vehicle(
            type=vehicle_type,
            model=f"{vehicle_object['Make']} {vehicle_object['Model']}",
            year=int(vehicle_object["Year"]),
            price=round(random.uniform(1000, 100000), 2),
        )
        policies.append(policy)
        vehicles.append(vehicle)

    return policies, vehicles


def generate_incident():
    accident_date = datetime.now() - relativedelta(years=1)
    file_date = accident_date + relativedelta(days=int(np.random.poisson(0.6, 1)))
    incident = Incident(accident_date=accident_date, file_date=file_date)

    claims = []
    payments = []
    injuries = []
    for _ in range(random.randint(1, 5)):
        claim = Claim(fraud=bool(random.random() < 0.03))

        claim_payment = None
        if random.random() < 0.8:
            if random.random() < 0.7:
                payed = claim.amount
            else:
                payed = round(random.random() * claim.amount, 2)
            claim_payment = ClaimPayment(amount=payed)

        payments.append(claim_payment)

        injury = None
        if random.random() < 0.3:
            injury = Injury()

        injuries.append(injury)

        claims.append(claim)

    return (
        incident,
        claims,
        payments,
        injuries,
    )


def generate_dataset():
    print("Data generation started...")
    individual_to_address = {}
    policy_to_individual = {}
    policy_to_vehicle = {}

    total_families = int(sys.argv[1])
    total_incidents = int(sys.argv[2])

    for _ in range(total_families):
        indvs, address = generate_family()
        store_address(address)

        for ind in indvs.copy():
            # Store individual on family address
            store_individual(ind, address)

            indvs.pop()
            individual_to_address[ind] = address
            policies, vehicles = generate_policy(ind)

            for policy, vehicle in zip(policies, vehicles):
                policy_to_individual[policy] = ind
                policy_to_vehicle[policy] = vehicle

                insured_with = (
                    random.choice(indvs) if random.random() < 0.7 and indvs else None
                )

                if random.random() < 0.9:
                    policy_address = address
                else:
                    policy_address = random_address()
                    # Store non-existing address in table
                    store_address(policy_address)

                # Store policy
                store_policy(policy, ind, vehicle, policy_address, insured_with)
                store_vehicle(vehicle)

            indvs.append(indvs)

    individuals = list(individual_to_address.keys())
    policies = list(policy_to_individual.keys())
    addresses = list(individual_to_address.values())

    for _ in range(total_incidents):
        incident, claims, payments, injuries = generate_incident()
        policy = random.choice(policies)
        policy_owner = policy_to_individual[policy]

        incident_inds = random.sample(
            individuals, min(len(individuals), random.randint(0, 3))
        )

        if random.random() < 0.2:
            incident_address = individual_to_address[policy_owner]
        else:
            if random.random() < 0.2:
                incident_address = random.choice(addresses)
            else:
                incident_address = random_address()

            # Store non-existing address in table
            store_address(incident_address)

        store_incident(
            incident,
            policy,
            incident_address,
            [
                (i, random.choice(["DRIVER", "WITNESS", "PEDESTRIAN", "PASSENGER"]))
                for i in incident_inds + [policy_owner]
            ],
        )

        for claim, payment, injury in zip(claims, payments, injuries):
            store_claim(claim, incident)
            if payment:
                store_claim_payment(
                    payment,
                    claim,
                    random.choice(incident_inds) if incident_inds else None,
                    policy_owner,
                )
            if injury:
                store_injury(
                    injury, claim, random.choice(incident_inds + [policy_owner])
                )

    dir_path = "dataset/data/"

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print("Created directory dataset/data")

    individual_data().to_parquet("dataset/data/" + "individuals.parquet")
    address_data().to_parquet("dataset/data/" + "/address.parquet")
    policy_data().to_parquet("dataset/data/" + "/policy.parquet")
    vehicle_data().to_parquet("dataset/data/" + "/vehicle.parquet")
    incident_data().to_parquet("dataset/data/" + "/incident.parquet")
    incident_individual_data().to_parquet("dataset/data/" + "/incident_individual.parquet")
    claim_data().to_parquet("dataset/data/" + "/claim.parquet")
    payment_data().to_parquet("dataset/data/" + "/claim_payment.parquet")
    injury_data().to_parquet("dataset/data/" + "/injury.parquet")
    print("Data stored in dataset/data !")


generate_dataset()
