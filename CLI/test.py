from functions import getFernetObj
x = "gAAAAABiDT5zCUWSi2auxJOE8T_Keuk6ae-ThYb8weZpv35Z94H1bhMBuu6RFEfFKhHBw2Si3y7OmSZ0r6gwtcRBbEtNEbfGixcG6SYB1xUNbzhOmLlymgH0OVz-8oqHVe7Yb3Up1MlqBfj3juP0kcR4K0p1cqDm6Q=="
print(getFernetObj("thunder","1234").decrypt(x.encode()))