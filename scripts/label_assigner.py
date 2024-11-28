import concurrent.futures as cf
from scripts.data_access import save_json_cache
import re as regex


def assign_labels(title, abstract, subfield_dict, max_labels=3):
    """
    Assign subfield labels to a paper based on its title and abstract, allowing multiple labels per paper.

    Args:
        title (str): The title of the paper.
        abstract (str): The abstract of the paper.
        subfield_dict (dict): A dictionary mapping keywords to subfields.
        max_labels (int): Maximum number of labels to assign.

    Returns:
        list: A list of assigned subfields, up to a specified maximum.
    """
    matched_subfields = []
    for keyword, subfield in subfield_dict.items():
        pattern = regex.compile(r'\b{}\b'.format(regex.escape(keyword)), regex.IGNORECASE)
        if pattern.search(title) or pattern.search(abstract):
            if subfield not in matched_subfields:
                matched_subfields.append(subfield)
            if len(matched_subfields) >= max_labels:
                break

    return matched_subfields if matched_subfields else ["Unknown"]


def create_subfield_dictionary():
    """
    Create a dictionary mapping keywords to subfield labels.
    
    Returns:
        dict: A dictionary of keywords and their corresponding subfields.
    """
    subfield_dict = {

        # General theoretical physics and others
        "anomaly": "General Theoretical Physics",
        "symmetry breaking": "General Theoretical Physics",

        # CKM Matrix (Related to Electroweak Physics and BSM)
        "CKM matrix": "Electroweak Physics",
        "CKM unitarity": "Electroweak Physics",
        "Vub": "Electroweak Physics",
        "Vcb": "Electroweak Physics",
        "unitarity triangle": "Electroweak Physics",
        "B meson": "Electroweak Physics",
        "B0 meson": "Electroweak Physics",
        "CP violation": "Electroweak Physics",
        "epsilon_K": "Electroweak Physics",
        "B0_s": "Electroweak Physics",

        # Supersymmetry (SUSY)
        "SUSY": "Supersymmetry",
        "supersymmetric": "Supersymmetry",
        "superpartner": "Supersymmetry",
        "sparticle": "Supersymmetry",
        "neutralino": "Supersymmetry",
        "squark": "Supersymmetry",
        "slepton": "Supersymmetry",

        # Gravitational Physics
        "gravity": "Gravitational Physics",
        "gravitational wave": "Gravitational Physics",
        "general relativity": "Gravitational Physics",
        "graviton": "Gravitational Physics",
        "curvature": "Gravitational Physics",
        "black hole": "Gravitational Physics",
        "cosmic string": "Gravitational Physics",

        # String Theory
        "string theory": "String Theory",
        "brane": "String Theory",
        "superstring": "String Theory",
        "M-theory": "String Theory",
        "tachyon": "String Theory",

        # Cosmology
        "inflation": "Cosmology",
        "dark matter": "Cosmology",
        "dark energy": "Cosmology",
        "cosmic microwave background": "Cosmology",
        "cosmology": "Cosmology",
        "big bang": "Cosmology",
        "early universe": "Cosmology",
        "scalar field": "Cosmology",

        # Neutrino Physics
        "neutrino": "Neutrino Physics",
        "neutrino oscillation": "Neutrino Physics",
        "lepton": "Neutrino Physics",
        "weak interaction": "Neutrino Physics",
        "sterile neutrino": "Neutrino Physics",
        "muon": "Neutrino Physics",

        # Electroweak Physics
        "electroweak": "Electroweak Physics",
        "Z boson": "Electroweak Physics",
        "W boson": "Electroweak Physics",
        "Higgs": "Electroweak Physics",
        "gauge symmetry": "Electroweak Physics",
        "radiative decay": "Electroweak Physics",
        "photon": "Electroweak Physics",
        "vector boson": "Electroweak Physics",
        "gauge boson": "Electroweak Physics",

        # Beyond the Standard Model (BSM)
        "Beyond the Standard Model": "Beyond the Standard Model",
        "BSM": "Beyond the Standard Model",  
        "effective Lagrangian": "Beyond the Standard Model",
        "grand unification": "Beyond the Standard Model",
        "extra dimension": "Beyond the Standard Model",
        "axion": "Beyond the Standard Model",
        "dark sector": "Beyond the Standard Model",
        "flavor physics": "Beyond the Standard Model",
        "technicolor": "Beyond the Standard Model",
        "leptoquark": "Beyond the Standard Model",
        "new physics": "Beyond the Standard Model",

        # Quantum Field Theory (QFT)
        "quantum field theory": "Quantum Field Theory",
        "gauge theory": "Quantum Field Theory",
        "renormalization": "Quantum Field Theory",
        "Feynman diagram": "Quantum Field Theory",
        "effective field theory": "Quantum Field Theory",
        "path integral": "Quantum Field Theory",
        "scalar field theory": "Quantum Field Theory",
        "chiral symmetry": "Quantum Field Theory",

        # High-Energy Physics (HEP)
        "PYTHIA": "Particle Physics",  
        "event generator": "Particle Physics",  
        "Monte Carlo": "Particle Physics",
        "CORSIKA": "Particle Physics",  
        "cosmic ray": "Particle Physics",  
        "hadron collider": "Particle Physics",
        "LHC": "Particle Physics",  
        "collider": "Particle Physics",

        # Quantum Electrodynamics (QED)
        "electron g-2": "Quantum Electrodynamics",  
        "QED": "Quantum Electrodynamics",
        "three-loop": "Quantum Electrodynamics",
        "loop calculation": "Quantum Electrodynamics",

        # Miscellaneous
        "penguin diagram": "Particle Physics",
        "collider": "Particle Physics",
        "asymmetry": "Particle Physics",
        "anomaly": "General Theoretical Physics",
        "symmetry breaking": "General Theoretical Physics",

        # Detailed QCD Subfields
        "Perturbative QCD": "Perturbative QCD",
        "high-energy collisions": "Perturbative QCD",
        "parton distribution functions": "Perturbative QCD",
        "Lattice QCD": "Non-Perturbative QCD",
        "chiral symmetry breaking": "Non-Perturbative QCD",
        "confinement": "Non-Perturbative QCD",
        "QCD phenomenology": "Phenomenology of QCD",
        "jet physics": "Phenomenology of QCD",
        "heavy ion collisions": "Phenomenology of QCD",
        "deep inelastic scattering": "Experimental QCD",
        "Drell-Yan": "Experimental QCD",
        "QCD experiments": "Experimental QCD",

        # General QCD
        "QCD": "Quantum Chromodynamics",
        "quark": "Quantum Chromodynamics",
        "gluon": "Quantum Chromodynamics",
        "hadron": "Quantum Chromodynamics",
        "strong interaction": "Quantum Chromodynamics",
        "meson": "Quantum Chromodynamics",
        "mesons": "Quantum Chromodynamics",
        "vector meson": "Quantum Chromodynamics",
        "spin-1": "Quantum Chromodynamics",
        "color confinement": "Quantum Chromodynamics",
        "baryon": "Quantum Chromodynamics",
        "proton": "Quantum Chromodynamics",
        "neutron": "Quantum Chromodynamics",
        "nucleon": "Quantum Chromodynamics",
        
    }
    return subfield_dict


def label_paper(paper_id, metadata, subfield_dict, max_labels=3):
    """
    Label a paper with up to three subfields based on its title and abstract.

    Args:
        paper_id (str): The ID of the paper.
        metadata (dict): A dictionary containing the paper's metadata.
        subfield_dict (dict): A dictionary mapping keywords to subfields.
        max_labels (int): Maximum number of labels to assign.

    Returns:
        tuple: A tuple containing the paper ID and a list of assigned subfields.
    """
    title = metadata.get("title", "")
    abstract = metadata.get("abstract", "")
    labels = assign_labels(title, abstract, subfield_dict, max_labels)
    return paper_id, labels


def label_papers(metadata, subfield_dict, cache_file='labels_cache.json'):
    """
    Label all papers in the metadata dictionary using concurrent processing.

    Args:
        metadata (dict): A dictionary where keys are paper IDs and values are their metadata.
        subfield_dict (dict): A dictionary mapping keywords to subfields.
        cache_file (str): The path to the cache file for storing labels.

    Returns:
        dict: A dictionary mapping paper IDs to lists of labels.
    """
    labeled_papers = {}
    with cf.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(label_paper, pid, metadata[pid], subfield_dict): pid for pid in metadata}
        for future in cf.as_completed(futures):
            paper_id, labels = future.result()
            labeled_papers[paper_id] = labels

    save_json_cache(labeled_papers, cache_file, "labels")
    return labeled_papers

    
