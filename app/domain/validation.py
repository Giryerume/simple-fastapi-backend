import re

from validate_docbr import CPF, PIS

cpf_validator = CPF()
pis_validator = PIS()


def validate_password(password: str, confirm: str) -> bool:
    if password == confirm:
        return True
    return False


def validate_email(email: str, format_only: bool = True) -> bool:
    if not email_verify_format(email):
        return False

    if format_only:
        return True

    return False


def validate_cpf(cpf: str, format_only: bool = True) -> bool:
    if not cpf_verify_format(cpf):
        return False

    if format_only:
        return True

    return cpf_validator.validate(cpf)


def validate_pis(pis: str, format_only: bool = True) -> bool:
    if not pis_verify_format(pis):
        return False

    if format_only:
        return True

    return pis_validator.validate(pis)


def cpf_verify_format(cpf: str):
    # Verifica a formatação do CPF
    return re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf)


def pis_verify_format(cpf: str):
    # Verifica a formatação do CPF
    return re.match(r'\d{3}\.\d{5}\.\d{2}-\d{1}', cpf)


def email_verify_format(email: str):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email)
