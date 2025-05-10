# Rules for theoretical charge calculation based on connection level and project phase

# Mapping of connection level and phase to theoretical charge (NB JH)
THEORETICAL_CHARGE_RULES = {
    "Connexion EDI": {
        "Non démarré (nouveau projet)": 0,
        "Cadrage / Spécifications": 1,
        "Développement": 3,
        "Recette utilisateur": 4,
        "Recette interne": 4,
        "Pré-production": 5,
        "En production (VSR)": 6,
        "Terminé (VSR signée)": 6
    },
    "Semi Connexion": {
        "Non démarré (nouveau projet)": 0,
        "Cadrage / Spécifications": 0.5,
        "Développement": 1,
        "Recette utilisateur": 2,
        "Recette interne": 2,
        "Pré-production": 3,
        "En production (VSR)": 4,
        "Terminé (VSR signée)": 4
    },
    "Normée": {
        "Non démarré (nouveau projet)": 0,
        "Cadrage / Spécifications": 0.25,
        "Développement": 0.25,
        "Recette utilisateur": 0.25,
        "Recette interne": 0.25,
        "Pré-production": 0.25,
        "En production (VSR)": 0.5,
        "Terminé (VSR signée)": 0.5
    },
    "Normée +": {
        "Non démarré (nouveau projet)": 0,
        "Cadrage / Spécifications": 0.25,
        "Développement": 0.25,
        "Recette utilisateur": 0.5,
        "Recette interne": 0.5,
        "Pré-production": 0.75,
        "En production (VSR)": 1,
        "Terminé (VSR signée)": 1
    },
    "Connexion EDI Pilote": {
        "Non démarré (nouveau projet)": 0,
        "Cadrage / Spécifications": 1,
        "Développement": 3,
        "Recette utilisateur": 4,
        "Recette interne": 4,
        "Pré-production": 5,
        "En production (VSR)": 10,
        "Terminé (VSR signée)": 10
    },
    "Connexion EDI GIS": {
        "Non démarré (nouveau projet)": 0,
        "Cadrage / Spécifications": 1,
        "Développement": 2,
        "Recette utilisateur": 4,
        "Recette interne": 4,
        "Pré-production": 6,
        "En production (VSR)": 7,
        "Terminé (VSR signée)": 7
    },
    "Connexion EDI Sortante": {
        "Non démarré (nouveau projet)": 0,
        "Cadrage / Spécifications": 1,
        "Développement": 2,
        "Recette utilisateur": 4,
        "Recette interne": 4,
        "Pré-production": 6,
        "En production (VSR)": 7,
        "Terminé (VSR signée)": 7
    }
}


def get_theoretical_charge(connection_level, project_phase):
    """
    Get the theoretical charge based on connection level and project phase.

    Args:
        connection_level (str): The connection level
        project_phase (str): The project phase

    Returns:
        float: The theoretical charge value, or None if no matching rule is found
    """
    # Handle empty values
    if not connection_level or not project_phase:
        return None

    # Special case for "Connexion EDI Sortante Pilote" - use "Connexion EDI Pilote" rules
    if connection_level == "Connexion EDI Sortante Pilote":
        connection_level = "Connexion EDI Pilote"

    # Check if connection level exists in rules
    if connection_level not in THEORETICAL_CHARGE_RULES:
        return None

    # Check if project phase exists for this connection level
    phase_rules = THEORETICAL_CHARGE_RULES[connection_level]
    if project_phase not in phase_rules:
        return None

    return phase_rules[project_phase]