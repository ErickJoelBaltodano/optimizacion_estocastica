import random

def mutacion_bit_flip(bits: str, prob_mut: float) -> str:
    """Invierte cada bit con probabilidad prob_mut."""
    return ''.join(
        ('1' if b=='0' else '0') if random.random() < prob_mut else b
        for b in bits
    )
