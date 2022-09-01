from typing import List, Tuple

from insurance import (
    Address,
    Claim,
    ClaimPayment,
    Incident,
    Individual,
    Injury,
    Policy,
    Vehicle,
)
import pandas as pd


policy_store = []
individual_store = []
address_store = []
vehicle_store = []

incident_store = []
claim_store = []
payment_store = []
injury_store = []

inc_ind_store = []


class IndividualField:
    IND_ID = "ind_id"
    IND_FNAME = "first_name"
    IND_LNAME = "last_name"
    IND_LIC = "driver_licence"
    IND_EXP = "years_experience"
    IND_PHO = "phone"


class AddressField:
    ADD_ID = "add_id"
    ADD_STR = "street_name"
    ADD_CIT = "city"
    ADD_COU = "country"


class VehicleField:
    VEH_ID = "veh_id"
    VEH_TYP = "type"
    VEH_MOD = "model"
    VEH_YEA = "year"
    VEH_PRI = "price"
    VEH_OWN = "owner_no"


class PolicyField:
    POL_ID = "pol_id"
    POL_SD = "start_date"
    POL_ED = "end_date"
    POL_TYP = "type"
    POL_PRE = "premium"


class IncidentField:
    INC_ID = "inc_id"
    INC_ACC = "accident_date"
    INC_FIL = "file_date"


class ClaimField:
    CLM_ID = "clm_id"
    CLM_FRD = "fraud"
    CLM_AMT = "amount"


class ClaimPaymentField:
    PAY_ID = "pay_id"
    PAY_AMT = "amount"


class InjuryField:
    INJ_ID = "inj_id"
    INJ_TYP = "type"


def store_individual(individual: Individual, address: Address):
    individual_store.append(
        [
            individual.id,
            individual.first_name,
            individual.last_name,
            individual.drivers_licence,
            individual.years_experience,
            individual.phone,
            address.id,
        ]
    )


def individual_data():
    return pd.DataFrame(
        individual_store,
        columns=[
            IndividualField.IND_ID,
            IndividualField.IND_FNAME,
            IndividualField.IND_LNAME,
            IndividualField.IND_LIC,
            IndividualField.IND_EXP,
            IndividualField.IND_PHO,
            AddressField.ADD_ID,
        ],
    )


def store_policy(
    policy: Policy,
    insurer: Individual,
    vehicle: Vehicle,
    address: Address,
    insured_with: Individual = None,
):
    policy_store.append(
        [
            policy.id,
            policy.start_date,
            policy.end_date,
            policy.type,
            policy.premium,
            insurer.id,
            insured_with.id if insured_with else None,
            vehicle.id,
            address.id,
        ]
    )


def policy_data():
    return pd.DataFrame(
        policy_store,
        columns=[
            PolicyField.POL_ID,
            PolicyField.POL_SD,
            PolicyField.POL_ED,
            PolicyField.POL_TYP,
            PolicyField.POL_PRE,
            "insurer_id",
            "insured_with_id",
            VehicleField.VEH_ID,
            AddressField.ADD_ID,
        ],
    )


def store_address(address: Address):
    address_store.append(
        [address.id, address.street_name, address.city, address.country]
    )


def address_data():
    return pd.DataFrame(
        address_store,
        columns=[
            AddressField.ADD_ID,
            AddressField.ADD_STR,
            AddressField.ADD_CIT,
            AddressField.ADD_COU,
        ],
    )


def store_vehicle(vehicle: Vehicle):
    vehicle_store.append(
        [
            vehicle.id,
            vehicle.type,
            vehicle.model,
            vehicle.year,
            vehicle.price,
            vehicle.owner_no,
        ]
    )


def vehicle_data():
    return pd.DataFrame(
        vehicle_store,
        columns=[
            VehicleField.VEH_ID,
            VehicleField.VEH_TYP,
            VehicleField.VEH_MOD,
            VehicleField.VEH_YEA,
            VehicleField.VEH_PRI,
            VehicleField.VEH_OWN,
        ],
    )


def store_incident(
    incident: Incident,
    policy: Policy,
    address: Address,
    relations: List[Tuple[Individual, str]],
):
    for ind, rel in relations:
        inc_ind_store.append([incident.id, ind.id, rel])

    incident_store.append(
        [incident.id, incident.accident_date, incident.file_date, policy.id, address.id]
    )


def incident_data():
    return pd.DataFrame(
        incident_store,
        columns=[
            IncidentField.INC_ID,
            IncidentField.INC_ACC,
            IncidentField.INC_FIL,
            PolicyField.POL_ID,
            AddressField.ADD_ID,
        ],
    )


def incident_individual_data():
    return pd.DataFrame(
        inc_ind_store,
        columns=[IncidentField.INC_ID, IndividualField.IND_ID, "relation"],
    )


def store_claim(claim: Claim, incident: Incident):
    claim_store.append([claim.id, claim.amount, claim.fraud, incident.id])


def claim_data():
    return pd.DataFrame(
        claim_store,
        columns=[
            ClaimField.CLM_ID,
            ClaimField.CLM_AMT,
            ClaimField.CLM_FRD,
            IncidentField.INC_ID,
        ],
    )


def store_claim_payment(
    claim_payment: ClaimPayment,
    claim: Claim,
    payer: Individual = None,
    payee: Individual = None,
):
    payment_store.append(
        [
            claim_payment.id,
            claim_payment.amount,
            claim.id,
            payer.id if payer else "",
            payee.id,
        ]
    )


def payment_data():
    return pd.DataFrame(
        payment_store,
        columns=[
            ClaimPaymentField.PAY_ID,
            ClaimPaymentField.PAY_AMT,
            ClaimField.CLM_ID,
            "payer_id",
            "payee_id",
        ],
    )


def store_injury(injury: Injury, claim: Claim, individual: Individual):
    injury_store.append([injury.id, injury.type, claim.id, individual.id])


def injury_data():
    return pd.DataFrame(
        injury_store,
        columns=[
            InjuryField.INJ_ID,
            InjuryField.INJ_TYP,
            ClaimField.CLM_ID,
            IndividualField.IND_ID,
        ],
    )
