def var_etat_A(PIB, nb_init) :
    """int * int -> int
    retourne l'evolution du nombres de millionaires au lieu A de t a t+1 sans compter les migrations"""

    #nb : int
    nb = 0 

    if PIB >= 15000  :
        nb = nb_init * 1.07

    elif PIB <= 4000  :
        nb = nb_init * 1.005
        
    else : 
        nb = nb_init * 1.03


    return int(nb) 
    
    
def var_A(PIB, pop_init, n): 
    """int*int*int -> list[int] """
    #A : int
    A = pop_init
    #a : list[int] 
    a = [pop_init]
    #i : int 
    for i in range(0, n) :
        A = var_etat_A(PIB, A)
        a.append(A)
        
    return a
    
    
def var_etat_B( nb_init) :
    """int  -> float
    retourne l'evolution du nombres de millionaires au lieu A de t a t+1"""
    return int (1.1 * nb_init)
    

def var_B(pop_init, n): 
    """int*int*int -> list[int] """
    #A : int
    A = pop_init
    #a : list[int] 
    a = [pop_init]
    #i : int 
    for i in range(0, n) :
        A = var_etat_B(A)
        a.append(A)
        
    return a
    

def passage_de_A_B (ind_eduA, ind_eduB, ind_secA, ind_secB) :
    
    """float**4 -> float
    calcul la probabilité qu'un millionaires qui quitte son pays A pour vivre vers B en fonction des
    conditions sociales de A et de B """
    
    #ind_social_A : float
    ind_social_A = ind_eduA + ind_secA

    #ind_social_B : float
    ind_social_B = ind_eduB + ind_secB

    #prob_A_vers_B : float
    prob_A_vers_B = 0.0 

    if ind_social_A < 110 and ind_social_A > 80 :
        if  ind_social_B > ind_social_A and ind_social_B < 160 :
             prob_A_vers_B = 0.02

        else :
            if ind_social_B > 160 :
                prob_A_vers_B = 0.035

    else :
        if  ind_social_B > ind_social_A and ind_social_B < 160 :
             prob_A_vers_B = 0.13

        else :
            if ind_social_B > 160 : 
                prob_A_vers_B = 0.32
            
    return prob_A_vers_B
    
    
def liste_depart(n, pop_init, ind_secuA, ind_eduA, ind_secuB, ind_eduB) : 
    """int * int * (float ** 4) -> liste[int]"""
    #res : liste[int]
    res = []
    #nb : int
    nb = pop_init
    #i : int 
    for i in range(0, n) : 
        res.append(int(nb*passage_de_A_B(ind_eduA, ind_eduB, ind_secuA, ind_secuB)))
        temp = var_etat_A(PIB, nb) 
        nb = temp - temp*passage_de_A_B(ind_eduA, ind_eduB, ind_secuA, ind_secuB)  
        
    return res
    

def passage_de_B_C (taux_impotB, taux_impotC, ind_eduC, ind_secC, patrimoine) : 
    """ float ** 5 -> float
    retourne la probabilité qu'un millionaire de la zone B (zone developpée) aille vivre sur C pour des raisons
    fiscales mais aussi eduction et niveau de vie"""

    #ind_social_C : float
    ind_social_C = ind_eduC + ind_secC

    #prob_B_vers_C : float
    prob_B_vers_C = 0.0


    if patrimoine <= 10.0 and patrimoine >= 1.0 : 
        if taux_impotB >= 0.55 and taux_impotC < 0.2 :
            if ind_social_C > 160.0:
              prob_B_vers_C = 0.08
            else :
              prob_B_vers_C = 0.02
              
        else :
            if taux_impotC <= taux_impotB - 0.15 :
                if ind_social_C > 160.0:
                  prob_B_vers_C = 0.06
                else :
                  prob_B_vers_C = 0.011


    
    else : 
        if taux_impotB >= 0.6 and taux_impotC <= taux_impotB - 0.15 :
            if ind_social_C > 160 :
              prob_B_vers_C = 0.11
            else :
              prob_B_vers_C = 0.008
              
        if taux_impotB > 0.4 and taux_impotB < 0.6 and taux_impotC <= taux_impotB - 0.15:
            if ind_social_C > 160 :
              prob_B_vers_C = 0.05
            else :
              prob_B_vers_C = 0.005
            

    return prob_B_vers_C
    
def liste_depart_BC(n, pop_init, taux_impotB, ind_eduC, ind_secuC, taux_impotC, patrimoine, ind_secuA, ind_eduA, ind_secuB, ind_eduB) : 
    """int * int * (float ** 4) *int * int *int *int  -> liste[int]"""
    
    #res : liste[int]
    res = []
    #nb : int
    nb = pop_init
    #e : int 
    e = 0 
    #i : int 
    for i in range(0, n) : 
    	e = int(nb * passage_de_B_C(taux_impotB, taux_impotC, ind_eduC, ind_secuC, patrimoine))
        res.append(e)
        temp = var_etat_B(nb - e)
        nb = temp + liste_depart(n, pop_init, ind_secuA, ind_eduA, ind_secuB, ind_eduB)[i]
        
    return res
    
    
def evolution_tot(n) :
    """ int-> dict[str : int]
    retourne le nombre de riches en A, B, C au bout de n années """
    
    #int : n_final_A
    n_final_A = nb_A
    #int : n_final_B
    n_final_B = nb_B
    #int : n_final_C
    n_final_C = nb_C
    #res : dict[str : int]
    res = dict() 
    
    #i : int 
    for i in range(0, n) :
        
        n_final_A = var_etat_A(PIB, n_final_A)
        n_final_A = n_final_A - n_final_A * passage_de_A_B (ind_eduA, ind_eduB, ind_secA, ind_secB)
        
        
        n_final_B = var_etat_B(n_final_B)
        n_final_B = n_final_B  - (n_final_B  * passage_de_B_C (taux_impotB, taux_impotC, ind_eduC, ind_secC, patrimoine)) + var_etat_A(PIB, nb_A) * passage_de_A_B (ind_eduA, ind_eduB, ind_secA, ind_secB)
        
        
        n_final_C = n_final_C + n_final_B  * passage_de_B_C (taux_impotB, taux_impotC, ind_eduC, ind_secC, patrimoine)
       


    res["A"] = int(n_final_A)
    res["B"] = int(n_final_B)
    res["C"] = int(n_final_C)

    return res




