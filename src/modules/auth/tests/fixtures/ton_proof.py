import pytest

from src.modules.auth.dto import Domain, ProofDTO, ProofVerificationDTO


@pytest.fixture
def ton_proof_data_request() -> ProofVerificationDTO:
    return ProofVerificationDTO(
        address="0:27bdfc252e6bd25eb499550ad313ba7df0c0cdfeafcc7b4c46f2f96a4de83f06",
        network=-239,
        proof=ProofDTO(
            timestamp=12,
            payload="",
            signature="",
            state_init="",
            domain=Domain(
                lengthBytes=21,
                value="ton-connect.github.io"
            )
        )
    )
