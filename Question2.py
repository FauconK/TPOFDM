# -*- coding: utf-8 -*-
# Nom du fichier: Question2.py
# Ce script implémente la chaîne de transmission OFDM
import numpy as np
import matplotlib.pyplot as plt

import ofdm_fonctions as ofdm

################################################################################
# Définition des paramètres de la transmission
################################################################################
# duree utile (s)
Tu=224e-6
# nombre total de porteuses
N=2048
# indice de la premiere sous-porteuse utile
Kmin=0
# indice de la derniere sous-porteuse utile
Kmax=1704
# periode d'échantillonnage (s)
Ts=Tu/N
print("Ts ="+str(Ts))
# duree de l'intervalle de garde (s)
Delta=Tu/8
print("Delta" + str(Delta))
# nombre d'échantillons de l'intervalle de garde 
L=int(Delta/Ts)
print("L"+str(L))
# indices des porteuses pilotes = 0,12,24,..,Kmax
PP=np.arange(0,Kmax+1,12)
print("PP"+str(PP))

# Espacement entre sous-porteuses (Hz)
Cs=1/Tu
print("Cs"+str(Cs))
# Largeur de la bande utile (Hz)
B=(Kmax-Kmin+1)*Cs
print("B"+str(B))

# Energie moyenne par symbole QPSK
Es=1
# Energie moyenne par symbole OFDM
E=Es*(Kmax-Kmin+1)
print("E"+str(E))
# Rapport signal-sur-bruit (dB)
EsN0dB=20
# Rapport signal-sur-bruit (échelle linéaire)
EsN0=np.power(10,EsN0dB/10)
# Densité spectrale monolatérale du bruit
N0=Es/EsN0
print("N0"+str(N0))
# retard (s) correspondant a un délai de propagation de 10 km 
tau=10e3/3e8
print("Tau"+str(tau))
# nombre d'échantillons retardés
theta=int(np.floor(tau/Ts))
print("Theta"+str(theta))
# retard fractionnaire
e=(tau-theta*Ts)/Ts
print("e"+str(e))

# décalage en frequence (Hz)
Df=1000.0
# nombre de symboles OFDM
T=2

# initialiser le signal émis 
s = np.array([])
# initialiser les symboles QPSK émis 
symb_QPSK = np.array([])
# pour chaque symbole OFDM
for i in range(T):
    # génération des symboles QPSK pour les 1705 sous-porteuses non-éteintes
    QPSK=ofdm.gen_QPSK(Kmax-Kmin+1)
    # concaténation des symboles QPSK
    symb_QPSK=np.append(symb_QPSK,QPSK)
    # modulation OFDM et introduction du retard fractionnaire
    m=ofdm.modulation_OFDM(np.sqrt(Es)*QPSK,N,L,e)
    # concaténation des symboles OFDM
    s=np.append(s,m)

# introduction du retard
s=np.append(np.zeros(theta),s)
# introduction du décalage en fréquence 
t=np.arange(len(s))*Ts
s=s*np.exp(1j*2.0*np.pi*Df*t)
# génération de la réponse impulsionnelle du canal 
# (Dirac ou Rayleigh avec profil d'intensité exponentiellement décroissant)
# d'étalement temporel Tm échantillons
Tm=100
c=ofdm.reponse_canal(L,1,Tm)

# génération d'un BABG complexe centré de variance N0
n=np.random.normal(0,np.sqrt(N0/2),size=len(s)+len(c)-1)+\
    1j*np.random.normal(0,np.sqrt(N0/2),size=len(s)+len(c)-1)
# signal recu dans le domaine temporel
y=np.convolve(s,c)+n

###########################################################
# Tracé de la réponse impulsionnelle du canal
###########################################################
# tracé de la partie réelle de la réponse impulsionnelle du canal
t=np.arange(len(c))*Ts
plt.stem(t,np.real(c),markerfmt='rD')
# tracé de la partie réelle de la réponse impulsionnelle du canal
plt.stem(t,np.imag(c),markerfmt='rD')
plt.xlabel('retard (s)')
plt.ylabel('réponse impulsionnelle du canal')
plt.show()
###########################################################
# Tracé de la réponse fréquentielle du canal
###########################################################
# axe fréquentiel
f=np.arange(N)/N*(1/Ts)
# calcul de la réponse fréquentielle du canal
H=np.fft.fft(c,N)
# tracé du module au carré de la réponse fréquentielle du canal
plt.stem(f,np.abs(H)**2,markerfmt='D')
plt.xlabel('fréquence (Hz)')
plt.ylabel('module au carré de la réponse fréquentielle du canal')
plt.show()
# tracé dela phase de la réponse fréquentielle du canal
plt.stem(f,np.angle(H)**2,markerfmt='rD')
plt.xlabel('fréquence (Hz)')
plt.ylabel('phase de la réponse fréquentielle du canal')
plt.show()