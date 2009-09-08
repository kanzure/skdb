"""Render a molecule in SMILES format using GraphViz.
based on a work by Brian Kelley. New BSD license
requires frowns: http://frowns.sf.net/
"""
import os, re
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class Error(Exception): pass

def generate_dot(mol_list):
    """(mol) Assign x,y coordinates to the atoms of a molecule
    using AT&T's graph layout algorithm.  This technique is
    very fast but doesn't look very good so use with
    caution."""

    
    ofile = StringIO()
    print >> ofile, "graph TEST {"
    
    d = {}
    for mol in mol_list:
      atoms = mol.atoms
      bonds = mol.bonds
      for atom in mol.atoms:
        d["atom%d"%atom.handle] = atom
        print >> ofile, '\tatom%s [\n\t  label="%s"\n\t\n\t  shape=none];' % (atom.handle, atom.symbol)
      for bond in mol.bonds:
        atom1, atom2 = bond.atoms
        
        print >> ofile, "\tatom%s -- atom%s;"%(atom1.handle, atom2.handle)
         
    print >> ofile, "}"

    return ofile.getvalue()

if __name__ == '__main__':
    from frowns import Smiles

    # read in a molecule
    smiles = ["c1ccccc1C=O",
            "c1ccc2cc1cccc2",
            "CCN",
            "CCCC(=O)NNCC",
            "CCC(CC)([CH](OC(N)=O)C1=CC=CC=C1)C2=CC=CC=C2",
            "ON=C(CC1=CC=CC=C1)[CH](C#N)C2=CC=CC=C2",
            "C1=CC=C(C=C1)C(N=C(C2=CC=CC=C2)C3=CC=CC=C3)C4=CC=CC=C4",
            ]


    mol_list = []
    for smile in smiles:
        mol = Smiles.smilin(smile)
        mol.name = smile
        mol_list.append(mol)

    f = open('frowns.dot', 'w')
    f.write(generate_dot(mol_list))

